"""IPEADATA API ingestion."""

import os
import time

import pandas as pd
import requests

from config import IPEADATA_SERIES, OUTPUT_DIR


def fetch_series(key, cfg):
    print(f"  [{key}] Fetching IPEADATA series {cfg['code']}...")
    url = f"http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{cfg['code']}')"
    try:
        r = requests.get(url, timeout=60, params={"$format": "json"})
        r.raise_for_status()
        data = r.json().get("value", [])
    except Exception as e:
        print(f"  [{key}] ERROR: {e}")
        return None

    if not data:
        print(f"  [{key}] No data.")
        return None

    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["VALDATA"], utc=True).dt.tz_localize(None)
    df["value"] = pd.to_numeric(df["VALVALOR"], errors="coerce")
    df = df.dropna(subset=["value"])
    df = df.set_index("date")[["value"]].rename(columns={"value": key})
    df = df.sort_index()
    print(f"  [{key}] Got {len(df)} records ({df.index.min().date()} to {df.index.max().date()}).")
    return df


def ingest_ipeadata():
    results = {}
    for key, cfg in IPEADATA_SERIES.items():
        print(f"\n--- IPEADATA: {key} ---")
        df = fetch_series(key, cfg)
        results[key] = (cfg, df)
        time.sleep(0.5)
    return results


def save_ipeadata_results(ipea_results):
    outdir = os.path.join(OUTPUT_DIR, "ipeadata")
    os.makedirs(outdir, exist_ok=True)

    daily_dfs, monthly_dfs = [], []
    for _, (cfg, df) in ipea_results.items():
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
