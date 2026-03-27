"""ComexStat (MDIC) Brazilian trade data ingestion via bulk CSV files.

Downloads raw export/import CSVs from MDIC, filters by NCM chapter,
and aggregates by product (SH4), country, and month.
"""

import io
import os
import time
import warnings

import pandas as pd
import requests

from config import COMEXSTAT_YEARS, COMEXSTAT_ORE_PRODUCTS, OUTPUT_DIR

warnings.filterwarnings("ignore", message="Unverified HTTPS")

BASE_URL = "https://balanca.economia.gov.br/balanca/bd/comexstat-bd/ncm"


def _download_year(flow, year):
    """Download a single year's export or import CSV from MDIC."""
    prefix = "EXP" if flow == "export" else "IMP"
    url = f"{BASE_URL}/{prefix}_{year}.csv"
    try:
        r = requests.get(url, timeout=120, verify=False)
        r.raise_for_status()
    except Exception as e:
        print(f"    [{prefix}_{year}] ERROR: {e}")
        return None

    df = pd.read_csv(
        io.StringIO(r.text),
        sep=";",
        dtype=str,
    )
    df.columns = df.columns.str.strip('"')
    for col in df.columns:
        df[col] = df[col].str.strip('"')

    df["KG_LIQUIDO"] = pd.to_numeric(df["KG_LIQUIDO"], errors="coerce")
    df["VL_FOB"] = pd.to_numeric(df["VL_FOB"], errors="coerce")
    df["date"] = pd.to_datetime(df["CO_ANO"] + "-" + df["CO_MES"].str.zfill(2) + "-01")
    df["SH4"] = df["CO_NCM"].str[:4]
    df["SH2"] = df["CO_NCM"].str[:2]
    print(f"    [{prefix}_{year}] {len(df)} records")
    return df


def _load_country_names():
    """Download country code mapping from MDIC."""
    url = "https://balanca.economia.gov.br/balanca/bd/tabelas/PAIS.csv"
    try:
        r = requests.get(url, timeout=30, verify=False)
        r.raise_for_status()
        df = pd.read_csv(io.StringIO(r.text), sep=";", dtype=str)
        df.columns = df.columns.str.strip('"')
        for col in df.columns:
            df[col] = df[col].str.strip('"')
        return dict(zip(df["CO_PAIS"], df["NO_PAIS"]))
    except Exception:
        return {}


def ingest_comexstat():
    """Download bulk CSVs and build filtered/aggregated DataFrames."""
    print("\n  Downloading country mapping...")
    country_map = _load_country_names()

    all_frames = []
    for year in COMEXSTAT_YEARS:
        print(f"\n  --- Year {year} ---")
        for flow in ["export", "import"]:
            df = _download_year(flow, year)
            if df is not None:
                df["flow"] = flow
                all_frames.append(df)
            time.sleep(0.5)

    if not all_frames:
        return {}

    raw = pd.concat(all_frames, ignore_index=True)

    # Filter to ore-related chapters (SH2 = 26, 72, 27, etc.)
    ore_sh2 = set()
    for cfg in COMEXSTAT_ORE_PRODUCTS.values():
        ore_sh2.update(cfg["sh2_codes"])
    raw_ores = raw[raw["SH2"].isin(ore_sh2)].copy()

    if country_map:
        raw_ores["country"] = raw_ores["CO_PAIS"].map(country_map).fillna(raw_ores["CO_PAIS"])

    results = {}

    # 1. Monthly totals by SH2 chapter and flow
    totals = (
        raw_ores.groupby(["date", "flow", "SH2"])
        .agg(fob_usd=("VL_FOB", "sum"), kg=("KG_LIQUIDO", "sum"))
        .reset_index()
    )
    totals_pivot = totals.pivot_table(
        index="date",
        columns=["flow", "SH2"],
        values=["fob_usd", "kg"],
        aggfunc="sum",
    )
    totals_pivot.columns = [f"{flow}_{sh2}_{metric}" for metric, flow, sh2 in totals_pivot.columns]
    totals_pivot = totals_pivot.sort_index()
    results["monthly_totals"] = totals_pivot

    # 2. Monthly by SH4 product (ore detail)
    sh4_agg = (
        raw_ores.groupby(["date", "flow", "SH4"])
        .agg(fob_usd=("VL_FOB", "sum"), kg=("KG_LIQUIDO", "sum"))
        .reset_index()
    )
    sh4_pivot = sh4_agg.pivot_table(
        index="date",
        columns=["flow", "SH4"],
        values=["fob_usd", "kg"],
        aggfunc="sum",
    )
    sh4_pivot.columns = [f"{flow}_{sh4}_{metric}" for metric, flow, sh4 in sh4_pivot.columns]
    sh4_pivot = sh4_pivot.sort_index()
    results["monthly_by_sh4"] = sh4_pivot

    # 3. Monthly exports by top destination countries (for chapter 26 only)
    exp_ores_26 = raw_ores[(raw_ores["SH2"] == "26") & (raw_ores["flow"] == "export")]
    if not exp_ores_26.empty and "country" in exp_ores_26.columns:
        country_agg = (
            exp_ores_26.groupby(["date", "country"])
            .agg(fob_usd=("VL_FOB", "sum"), kg=("KG_LIQUIDO", "sum"))
            .reset_index()
        )
        # Keep top 15 countries by total FOB
        top_countries = (
            country_agg.groupby("country")["fob_usd"].sum()
            .nlargest(15).index.tolist()
        )
        country_top = country_agg[country_agg["country"].isin(top_countries)]
        country_pivot = country_top.pivot_table(
            index="date", columns="country", values="fob_usd", aggfunc="sum"
        )
        country_pivot.columns = [f"exp_26_{c}_fob" for c in country_pivot.columns]
        country_pivot = country_pivot.sort_index()
        results["export_ores_by_country"] = country_pivot

    # Build config-like metadata for dictionary
    results_with_cfg = {}
    for rkey, df in results.items():
        results_with_cfg[rkey] = (
            {"name": f"ComexStat - {rkey}", "description": f"Brazilian trade data: {rkey}"},
            df,
        )

    return results_with_cfg


def save_comexstat_results(comex_results):
    outdir = os.path.join(OUTPUT_DIR, "comexstat")
    os.makedirs(outdir, exist_ok=True)

    for key, (cfg, df) in comex_results.items():
        if df is None or df.empty:
            continue
        filepath = os.path.join(outdir, f"{key}.csv")
        df.to_csv(filepath)
        print(f"  Saved {filepath} ({len(df)} rows, {len(df.columns)} cols)")
