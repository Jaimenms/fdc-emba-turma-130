"""
Ingestion package: one module per data source.

Usage:
    python -m ingestion                          # all sources
    python -m ingestion --sources sidra,bcb      # only SIDRA and BCB
    python -m ingestion --sources all            # all sources (explicit)
    python -m ingestion --list                   # list available sources
"""

import argparse
import os

from config import OUTPUT_DIR
from ingestion.sidra import ingest_sidra, save_sidra_results
from ingestion.bcb import ingest_bcb, save_bcb_results
from ingestion.ipeadata import ingest_ipeadata, save_ipeadata_results
from ingestion.comexstat import ingest_comexstat, save_comexstat_results
from ingestion.worldbank import ingest_worldbank, save_worldbank_results
from ingestion.investpy_minerals import ingest_investpy, save_investpy_results
from ingestion.dictionary import build_all_dictionaries

SOURCES = {
    "sidra":     ("SIDRA (IBGE)",                    ingest_sidra,     save_sidra_results),
    "bcb":       ("BCB (Banco Central)",             ingest_bcb,       save_bcb_results),
    "ipeadata":  ("IPEADATA",                        ingest_ipeadata,  save_ipeadata_results),
    "comexstat": ("ComexStat (MDIC)",                ingest_comexstat, save_comexstat_results),
    "worldbank": ("World Bank (WDI)",                ingest_worldbank, save_worldbank_results),
    "investpy":  ("investpy (Mineral Commodities)",  ingest_investpy,  save_investpy_results),
}


def parse_args():
    available = ",".join(SOURCES.keys())
    parser = argparse.ArgumentParser(
        description="Ingest economic data from multiple sources.",
        usage="python -m ingestion [sources] [--list]",
    )
    parser.add_argument(
        "sources",
        nargs="?",
        default=None,
        help=f"Comma-separated sources (default: all). Available: {available}",
    )
    parser.add_argument(
        "--sources",
        dest="sources_flag",
        default=None,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--list",
        action="store_true",
        dest="list_sources",
        help="List available sources and exit.",
    )
    args = parser.parse_args()
    # Accept both positional and --sources flag
    args.sources = args.sources_flag or args.sources or "all"
    return args


def main():
    args = parse_args()

    if args.list_sources:
        print("Available sources:")
        for key, (label, _, _) in SOURCES.items():
            print(f"  {key:12s} - {label}")
        return

    if args.sources.strip().lower() == "all":
        selected = list(SOURCES.keys())
    else:
        selected = [s.strip().lower() for s in args.sources.split(",") if s.strip()]
        invalid = [s for s in selected if s not in SOURCES]
        if invalid:
            print(f"ERROR: Unknown source(s): {', '.join(invalid)}")
            print(f"Available: {', '.join(SOURCES.keys())}")
            return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    total = len(selected)
    print("=" * 60)
    print(f"DATA INGESTION - {total} source(s): {', '.join(selected)}")
    print("=" * 60)

    results = {}
    for i, key in enumerate(selected, 1):
        label, ingest_fn, _ = SOURCES[key]
        print(f"\n{'=' * 60}")
        print(f"{i}/{total} - {label}")
        print("=" * 60)
        results[key] = ingest_fn()

    print(f"\n{'=' * 60}")
    print("Saving CSV files...")
    print("=" * 60)
    for key in selected:
        _, _, save_fn = SOURCES[key]
        save_fn(results[key])

    print("\nBuilding data dictionaries...")
    build_all_dictionaries(
        results.get("sidra", {}),
        results.get("bcb", {}),
        results.get("ipeadata", {}),
        results.get("comexstat", {}),
        results.get("worldbank", {}),
        results.get("investpy", {}),
    )

    print(f"\n{'=' * 60}")
    print("DONE! Output files:")
    print("=" * 60)
    for dirpath, _, filenames in sorted(os.walk(OUTPUT_DIR)):
        for fname in sorted(filenames):
            fpath = os.path.join(dirpath, fname)
            rel = os.path.relpath(fpath, OUTPUT_DIR)
            size_kb = os.path.getsize(fpath) / 1024
            print(f"  {rel} ({size_kb:.0f} KB)")
