"""Data dictionary builder — one dictionary JSON per CSV file, in source subfolders."""

import json
import os

from config import OUTPUT_DIR


def _save_dict(source, csv_basename, entries):
    """Save a dictionary JSON alongside a CSV in data/<source>/."""
    if not entries:
        return
    dict_filename = csv_basename.replace(".csv", ".dictionary.json")
    outdir = os.path.join(OUTPUT_DIR, source)
    os.makedirs(outdir, exist_ok=True)
    filepath = os.path.join(outdir, dict_filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
    print(f"  Saved {filepath} ({len(entries)} indicators)")


def build_sidra_dictionaries(sidra_results):
    by_file = {}
    for key, (cfg, df) in sidra_results.items():
        if df is None:
            continue
        freq = cfg["frequency"]
        csv_name = f"{freq}.csv"
        if csv_name not in by_file:
            by_file[csv_name] = []
        for col in df.columns:
            by_file[csv_name].append({
                "column": f"{key}__{col}",
                "indicator": col,
                "table_key": key,
                "table_code": cfg["table_code"],
                "table_name": cfg["name"],
                "description": cfg["description"],
                "source": cfg["source"],
                "frequency": freq,
                "unit": cfg["unit"],
                "calculation": cfg["calculation"],
            })
    for csv_name, entries in by_file.items():
        _save_dict("sidra", csv_name, entries)


def build_bcb_dictionaries(bcb_results):
    by_file = {}
    for key, (cfg, df) in bcb_results.items():
        if df is None:
            continue
        freq = "daily" if cfg["frequency"] == "daily" else "monthly"
        csv_name = f"{freq}.csv"
        if csv_name not in by_file:
            by_file[csv_name] = []
        by_file[csv_name].append({
            "column": key,
            "indicator": cfg["name"],
            "series_code": cfg["code"],
            "description": cfg["description"],
            "source": cfg["source"],
            "frequency": cfg["frequency"],
            "unit": cfg["unit"],
        })
    for csv_name, entries in by_file.items():
        _save_dict("bcb", csv_name, entries)


def build_ipeadata_dictionaries(ipea_results):
    by_file = {}
    for key, (cfg, df) in ipea_results.items():
        if df is None:
            continue
        freq = "daily" if cfg["frequency"] == "daily" else "monthly"
        csv_name = f"{freq}.csv"
        if csv_name not in by_file:
            by_file[csv_name] = []
        by_file[csv_name].append({
            "column": key,
            "indicator": cfg["name"],
            "series_code": cfg["code"],
            "description": cfg["description"],
            "source": cfg["source"],
            "frequency": cfg["frequency"],
            "unit": cfg["unit"],
        })
    for csv_name, entries in by_file.items():
        _save_dict("ipeadata", csv_name, entries)


def build_comexstat_dictionary(comex_results):
    for key, (cfg, df) in comex_results.items():
        if df is None or df.empty:
            continue
        entries = []
        for col in df.columns:
            unit = "US$ FOB" if "fob" in col.lower() else "kg"
            entries.append({
                "column": col,
                "indicator": col,
                "description": cfg.get("description", ""),
                "source": "MDIC - ComexStat (bulk CSV)",
                "frequency": "monthly",
                "unit": unit,
            })
        _save_dict("comexstat", f"{key}.csv", entries)


def build_worldbank_dictionary(wb_results):
    entries = []
    for key, (cfg, df) in wb_results.items():
        if df is None:
            continue
        for col in df.columns:
            country = col.split("__")[1] if "__" in col else col
            entries.append({
                "column": col,
                "indicator": f"{cfg['name']} - {country}",
                "wb_code": cfg["code"],
                "description": cfg["description"],
                "source": "World Bank - WDI",
                "frequency": "annual",
                "unit": "See indicator name",
            })
    _save_dict("worldbank", "annual.csv", entries)


def build_investpy_dictionary(investpy_results):
    entries = []
    if not investpy_results:
        return
    for key, (cfg, df) in investpy_results.items():
        if df is None:
            continue
        entries.append({
            "column": key,
            "indicator": cfg["name"],
            "commodity": cfg.get("commodity") or cfg.get("search_term", key),
            "description": cfg["description"],
            "source": cfg["source"],
            "frequency": "daily",
            "unit": cfg["unit"],
        })
    _save_dict("investpy", "daily.csv", entries)


def build_consolidated_dictionary():
    """Merge all per-source dictionary JSONs into a single data/dictionary.json.

    Each entry is enriched with a ``file`` field containing the relative path
    (from the data/ directory) to the CSV that holds the column.
    """
    consolidated = []
    for dirpath, _, filenames in sorted(os.walk(OUTPUT_DIR)):
        for fname in sorted(filenames):
            if not fname.endswith(".dictionary.json"):
                continue
            csv_name = fname.replace(".dictionary.json", ".csv")
            # Relative path from OUTPUT_DIR, e.g. "sidra/monthly.csv"
            rel_csv = os.path.relpath(os.path.join(dirpath, csv_name), OUTPUT_DIR)
            filepath = os.path.join(dirpath, fname)
            with open(filepath, "r", encoding="utf-8") as f:
                entries = json.load(f)
            for entry in entries:
                entry["file"] = rel_csv
                consolidated.append(entry)

    out_path = os.path.join(OUTPUT_DIR, "dictionary.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(consolidated, f, ensure_ascii=False, indent=2)
    print(f"  Saved {out_path} ({len(consolidated)} indicators consolidated)")


def build_all_dictionaries(sidra_results, bcb_results, ipea_results, comex_results, wb_results, investpy_results=None):
    """Build one dictionary JSON per CSV file, then consolidate into data/dictionary.json."""
    build_sidra_dictionaries(sidra_results)
    build_bcb_dictionaries(bcb_results)
    build_ipeadata_dictionaries(ipea_results)
    build_comexstat_dictionary(comex_results)
    build_worldbank_dictionary(wb_results)
    build_investpy_dictionary(investpy_results or {})
    build_consolidated_dictionary()
