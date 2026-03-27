"""SIDRA (IBGE) data ingestion."""

import os
import time

import pandas as pd
import sidrapy

from config import TABLES, OUTPUT_DIR


def fetch_table(key, cfg):
    print(f"  [{key}] Fetching SIDRA table {cfg['table_code']}...")
    params = {
        "table_code": cfg["table_code"],
        "territorial_level": cfg["territorial_level"],
        "ibge_territorial_code": cfg["ibge_territorial_code"],
        "period": cfg["period"],
        "header": "y",
    }
    if cfg.get("variable") and cfg["variable"] != "all":
        params["variable"] = cfg["variable"]
    if cfg.get("classifications"):
        params["classifications"] = cfg["classifications"]

    try:
        df = sidrapy.get_table(**params)
    except Exception as e:
        print(f"  [{key}] ERROR: {e}")
        return None

    if df is None or df.empty:
        print(f"  [{key}] No data returned.")
        return None

    df = df.iloc[1:].reset_index(drop=True)
    print(f"  [{key}] Got {len(df)} rows.")
    return df


def parse_period(period_str, frequency):
    if pd.isna(period_str) or not isinstance(period_str, str):
        return pd.NaT
    period_str = period_str.strip()
    try:
        if len(period_str) == 6 and period_str.isdigit():
            year, sub = int(period_str[:4]), int(period_str[4:6])
            month = (sub - 1) * 3 + 1 if frequency == "quarterly" else sub
            return pd.Timestamp(year=year, month=month, day=1)
        elif len(period_str) == 4 and period_str.isdigit():
            return pd.Timestamp(year=int(period_str), month=1, day=1)
    except (ValueError, TypeError):
        pass
    return pd.NaT


def process_table(key, cfg, raw_df):
    if "D2C" not in raw_df.columns or "V" not in raw_df.columns:
        print(f"  [{key}] Missing D2C or V columns.")
        return None

    raw_df = raw_df.copy()
    raw_df["date"] = raw_df["D2C"].apply(lambda x: parse_period(str(x), cfg["frequency"]))
    raw_df = raw_df.dropna(subset=["date"])
    if raw_df.empty:
        print(f"  [{key}] No valid dates.")
        return None

    raw_df["value"] = pd.to_numeric(
        raw_df["V"].astype(str).str.replace(",", ".").str.strip()
        .replace({"...": None, "-": None, "X": None, "..": None}),
        errors="coerce",
    )

    desc_cols = [c for c in raw_df.columns if c.startswith("D") and c.endswith("N") and c not in ("D1N", "D2N")]
    if desc_cols:
        raw_df["label"] = raw_df[desc_cols].astype(str).agg(" - ".join, axis=1)
    else:
        raw_df["label"] = key
    raw_df["label"] = raw_df["label"].str.strip(" -").str.replace(r"\s+", " ", regex=True)

    try:
        pivoted = raw_df.pivot_table(index="date", columns="label", values="value", aggfunc="first")
    except Exception as e:
        print(f"  [{key}] Pivot failed: {e}")
        return None

    pivoted = pivoted.sort_index()
    pivoted.index.name = "date"
    pivoted.columns = [str(c).strip() for c in pivoted.columns]
    print(f"  [{key}] Processed: {len(pivoted)} periods, {len(pivoted.columns)} indicators.")
    return pivoted


def ingest_sidra():
    results = {}
    for key, cfg in TABLES.items():
        print(f"\n--- SIDRA: {key} ---")
        raw_df = fetch_table(key, cfg)
        if raw_df is not None:
            results[key] = (cfg, process_table(key, cfg, raw_df))
        else:
            results[key] = (cfg, None)
        time.sleep(1)
    return results


def save_sidra_results(sidra_results):
    outdir = os.path.join(OUTPUT_DIR, "sidra")
    os.makedirs(outdir, exist_ok=True)

    freq_groups = {}
    for key, (cfg, df) in sidra_results.items():
        if df is None:
            continue
        freq = cfg["frequency"]
        if freq not in freq_groups:
            freq_groups[freq] = []
        prefixed = df.rename(columns={c: f"{key}__{c}" for c in df.columns})
        freq_groups[freq].append(prefixed)

    for freq, dfs in freq_groups.items():
        merged = pd.concat(dfs, axis=1, sort=True).sort_index()
        filepath = os.path.join(outdir, f"{freq}.csv")
        merged.to_csv(filepath, index=True)
        print(f"  Saved {filepath} ({len(merged)} rows, {len(merged.columns)} cols)")
