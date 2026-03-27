"""Mineral commodity prices via investpy (Investing.com)."""

import os
import time
import warnings

import pandas as pd

from config import INVESTPY_COMMODITIES, OUTPUT_DIR

warnings.filterwarnings("ignore", module="investpy")


def fetch_commodity(key, cfg):
    import investpy

    name = cfg.get("commodity") or cfg.get("search_term", key)
    print(f"  [{key}] Fetching {name}...")

    try:
        if "search_term" in cfg:
            # Use search_quotes API for commodities not in the standard list
            quote = investpy.search_quotes(
                text=cfg["search_term"],
                products=["commodities"],
                n_results=1,
            )
            df = quote.retrieve_historical_data(
                from_date=cfg.get("from_date", "01/01/2000"),
                to_date=cfg.get("to_date", "31/12/2026"),
            )
        else:
            df = investpy.commodities.get_commodity_historical_data(
                commodity=cfg["commodity"],
                from_date=cfg.get("from_date", "01/01/2000"),
                to_date=cfg.get("to_date", "31/12/2026"),
                country=cfg.get("country"),
            )
    except Exception as e:
        print(f"  [{key}] ERROR: {e}")
        return None

    if df is None or df.empty:
        print(f"  [{key}] No data.")
        return None

    df.index.name = "date"
    result = df[["Close"]].rename(columns={"Close": key})
    print(f"  [{key}] Got {len(result)} records ({result.index.min().date()} to {result.index.max().date()}).")
    return result


def ingest_investpy():
    results = {}
    for key, cfg in INVESTPY_COMMODITIES.items():
        print(f"\n--- investpy: {key} ---")
        df = fetch_commodity(key, cfg)
        results[key] = (cfg, df)
        time.sleep(1)
    return results


def save_investpy_results(investpy_results):
    outdir = os.path.join(OUTPUT_DIR, "investpy")
    os.makedirs(outdir, exist_ok=True)

    dfs = []
    for _, (_, df) in investpy_results.items():
        if df is not None:
            dfs.append(df[~df.index.duplicated(keep="last")])
    if dfs:
        merged = pd.concat(dfs, axis=1, sort=True).sort_index()
        filepath = os.path.join(outdir, "daily.csv")
        merged.to_csv(filepath)
        print(f"  Saved {filepath} ({len(merged)} rows, {len(merged.columns)} cols)")
