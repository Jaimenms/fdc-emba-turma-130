"""World Bank WDI data ingestion."""

import os
import time

import pandas as pd
import requests

from config import WORLDBANK_INDICATORS, WORLDBANK_COUNTRIES, OUTPUT_DIR


def fetch_indicator(key, cfg, countries):
    print(f"  [{key}] Fetching World Bank {cfg['code']}...")
    url = f"https://api.worldbank.org/v2/country/{countries}/indicator/{cfg['code']}"
    all_records = []
    page = 1
    while True:
        try:
            r = requests.get(url, params={"format": "json", "per_page": 500, "page": page}, timeout=60)
            r.raise_for_status()
            data = r.json()
        except Exception as e:
            print(f"  [{key}] ERROR: {e}")
            break

        if len(data) < 2 or not data[1]:
            break

        all_records.extend(data[1])
        total_pages = data[0].get("pages", 1)
        if page >= total_pages:
            break
        page += 1

    if not all_records:
        print(f"  [{key}] No data.")
        return None

    rows = []
    for rec in all_records:
        if rec["value"] is not None:
            rows.append({
                "year": int(rec["date"]),
                "country": rec["countryiso3code"],
                "value": rec["value"],
            })

    if not rows:
        print(f"  [{key}] All values null.")
        return None

    df = pd.DataFrame(rows)
    pivoted = df.pivot_table(index="year", columns="country", values="value", aggfunc="first")
    pivoted.columns = [f"{key}__{c}" for c in pivoted.columns]
    pivoted = pivoted.sort_index()
    pivoted.index.name = "year"
    print(f"  [{key}] Got {len(pivoted)} years, {len(pivoted.columns)} countries.")
    return pivoted


def ingest_worldbank():
    results = {}
    countries = WORLDBANK_COUNTRIES
    for key, cfg in WORLDBANK_INDICATORS.items():
        print(f"\n--- World Bank: {key} ---")
        df = fetch_indicator(key, cfg, countries)
        results[key] = (cfg, df)
        time.sleep(0.5)
    return results


def save_worldbank_results(wb_results):
    outdir = os.path.join(OUTPUT_DIR, "worldbank")
    os.makedirs(outdir, exist_ok=True)

    dfs = [df for _, (_, df) in wb_results.items() if df is not None]
    if dfs:
        merged = pd.concat(dfs, axis=1, sort=True).sort_index()
        filepath = os.path.join(outdir, "annual.csv")
        merged.to_csv(filepath)
        print(f"  Saved {filepath} ({len(merged)} rows, {len(merged.columns)} cols)")
