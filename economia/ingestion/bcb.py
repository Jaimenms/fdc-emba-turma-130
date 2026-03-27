"""BCB (Banco Central do Brasil) SGS API ingestion."""

import os
import time

import pandas as pd
import requests

from config import BCB_SERIES, OUTPUT_DIR


def _fetch_chunk(code, date_start, date_end):
    """Fetch a single date range from BCB SGS."""
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados"
    params = {"formato": "json", "dataInicial": date_start, "dataFinal": date_end}
    r = requests.get(url, params=params, timeout=120, headers={"Accept": "application/json"})
    r.raise_for_status()
    return r.json()


def fetch_series(key, cfg):
    print(f"  [{key}] Fetching BCB series {cfg['code']}...")

    # Daily series are too large for a single request — fetch in 5-year chunks
    all_data = []
    if cfg["frequency"] == "daily":
        for start_year in range(1990, 2027, 5):
            end_year = min(start_year + 4, 2026)
            try:
                chunk = _fetch_chunk(cfg["code"], f"01/01/{start_year}", f"31/12/{end_year}")
                if chunk:
                    all_data.extend(chunk)
            except Exception:
                pass
            time.sleep(0.3)
    else:
        try:
            all_data = _fetch_chunk(cfg["code"], "01/01/1990", "31/12/2026")
        except Exception as e:
            print(f"  [{key}] ERROR: {e}")
            return None

    if not all_data:
        print(f"  [{key}] No data.")
        return None

    df = pd.DataFrame(all_data)
    df["date"] = pd.to_datetime(df["data"], format="%d/%m/%Y")
    df["value"] = pd.to_numeric(df["valor"].str.replace(",", "."), errors="coerce")
    df = df.set_index("date")[["value"]].rename(columns={"value": key})
    df = df.sort_index()
    df = df[~df.index.duplicated(keep="last")]
    print(f"  [{key}] Got {len(df)} records ({df.index.min().date()} to {df.index.max().date()}).")
    return df


def ingest_bcb():
    results = {}
    for key, cfg in BCB_SERIES.items():
        print(f"\n--- BCB: {key} ---")
        df = fetch_series(key, cfg)
        results[key] = (cfg, df)
        time.sleep(0.5)
    return results


def save_bcb_results(bcb_results):
    outdir = os.path.join(OUTPUT_DIR, "bcb")
    os.makedirs(outdir, exist_ok=True)

    daily_dfs, monthly_dfs = [], []
    for _, (cfg, df) in bcb_results.items():
        if df is None:
            continue
        if cfg["frequency"] == "daily":
            daily_dfs.append(df)
        else:
            monthly_dfs.append(df)

    if daily_dfs:
        merged = pd.concat(daily_dfs, axis=1, sort=True).sort_index()
        filepath = os.path.join(outdir, "daily.csv")
        merged.to_csv(filepath)
        print(f"  Saved {filepath} ({len(merged)} rows, {len(merged.columns)} cols)")

    if monthly_dfs:
        merged = pd.concat(monthly_dfs, axis=1, sort=True).sort_index()
        filepath = os.path.join(outdir, "monthly.csv")
        merged.to_csv(filepath)
        print(f"  Saved {filepath} ({len(merged)} rows, {len(merged.columns)} cols)")
