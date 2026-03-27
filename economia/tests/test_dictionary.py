"""Tests for ingestion.dictionary module."""

import json
import pandas as pd
from unittest.mock import patch

from ingestion.dictionary import (
    build_sidra_dictionaries,
    build_bcb_dictionaries,
    build_comexstat_dictionary,
    build_investpy_dictionary,
    build_consolidated_dictionary,
    build_all_dictionaries,
)


class TestSidraDictionary:
    def test_creates_per_frequency_file(self, tmp_path):
        sidra = {
            "pib": (
                {
                    "table_code": "1620", "name": "PIB", "description": "GDP",
                    "source": "IBGE", "frequency": "quarterly",
                    "unit": "Index", "calculation": "Volume index",
                },
                pd.DataFrame({"GDP": [100]}, index=pd.DatetimeIndex(["2024-01-01"])),
            )
        }
        with patch("ingestion.dictionary.OUTPUT_DIR", str(tmp_path)):
            build_sidra_dictionaries(sidra)

        path = tmp_path / "sidra" / "quarterly.dictionary.json"
        assert path.exists()
        entries = json.loads(path.read_text())
        assert isinstance(entries, list)
        assert len(entries) == 1
        assert entries[0]["column"] == "pib__GDP"
        assert entries[0]["source"] == "IBGE"
        assert "file" not in entries[0]

    def test_skips_none(self, tmp_path):
        sidra = {"pib": ({"frequency": "quarterly"}, None)}
        with patch("ingestion.dictionary.OUTPUT_DIR", str(tmp_path)):
            build_sidra_dictionaries(sidra)
        assert not list(tmp_path.rglob("*.json"))


class TestBcbDictionary:
    def test_splits_daily_monthly(self, tmp_path):
        bcb = {
            "selic": (
                {"code": 432, "name": "SELIC", "description": "Rate", "source": "BCB", "frequency": "daily", "unit": "%"},
                pd.DataFrame({"selic": [14.75]}, index=pd.DatetimeIndex(["2024-01-01"])),
            ),
            "igpm": (
                {"code": 189, "name": "IGP-M", "description": "Inflation", "source": "BCB", "frequency": "monthly", "unit": "%"},
                pd.DataFrame({"igpm": [0.5]}, index=pd.DatetimeIndex(["2024-01-01"])),
            ),
        }
        with patch("ingestion.dictionary.OUTPUT_DIR", str(tmp_path)):
            build_bcb_dictionaries(bcb)

        daily = json.loads((tmp_path / "bcb" / "daily.dictionary.json").read_text())
        monthly = json.loads((tmp_path / "bcb" / "monthly.dictionary.json").read_text())
        assert isinstance(daily, list)
        assert len(daily) == 1
        assert daily[0]["column"] == "selic"
        assert len(monthly) == 1
        assert monthly[0]["column"] == "igpm"


class TestInvestpyDictionary:
    def test_includes_search_term_commodities(self, tmp_path):
        investpy = {
            "gold": (
                {"commodity": "Gold", "name": "Ouro", "description": "Gold price", "source": "investpy", "unit": "USD"},
                pd.DataFrame({"gold": [2000]}, index=pd.DatetimeIndex(["2024-01-01"])),
            ),
            "iron_ore": (
                {"search_term": "iron ore", "name": "Minério de ferro", "description": "Iron ore", "source": "investpy", "unit": "USD/ton"},
                pd.DataFrame({"iron_ore": [100]}, index=pd.DatetimeIndex(["2024-01-01"])),
            ),
        }
        with patch("ingestion.dictionary.OUTPUT_DIR", str(tmp_path)):
            build_investpy_dictionary(investpy)

        entries = json.loads((tmp_path / "investpy" / "daily.dictionary.json").read_text())
        assert isinstance(entries, list)
        assert len(entries) == 2
        gold = next(e for e in entries if e["column"] == "gold")
        iron = next(e for e in entries if e["column"] == "iron_ore")
        assert gold["commodity"] == "Gold"
        assert iron["commodity"] == "iron ore"


class TestComexstatDictionary:
    def test_creates_per_key_dictionary(self, tmp_path):
        comex = {
            "monthly_totals": (
                {"name": "ComexStat - monthly_totals", "description": "Trade totals"},
                pd.DataFrame(
                    {"export_26_fob_usd": [1e9], "export_26_kg": [1e10]},
                    index=pd.DatetimeIndex(["2024-01-01"]),
                ),
            )
        }
        with patch("ingestion.dictionary.OUTPUT_DIR", str(tmp_path)):
            build_comexstat_dictionary(comex)

        entries = json.loads((tmp_path / "comexstat" / "monthly_totals.dictionary.json").read_text())
        assert len(entries) == 2
        columns = [e["column"] for e in entries]
        assert "export_26_fob_usd" in columns
        assert "export_26_kg" in columns


class TestConsolidatedDictionary:
    def test_merges_all_sources_with_file_path(self, tmp_path):
        sidra = {
            "pib": (
                {
                    "table_code": "1620", "name": "PIB", "description": "GDP",
                    "source": "IBGE", "frequency": "quarterly",
                    "unit": "Index", "calculation": "Volume index",
                },
                pd.DataFrame({"GDP": [100]}, index=pd.DatetimeIndex(["2024-01-01"])),
            )
        }
        bcb = {
            "selic": (
                {"code": 432, "name": "SELIC", "description": "Rate", "source": "BCB", "frequency": "daily", "unit": "%"},
                pd.DataFrame({"selic": [14.75]}, index=pd.DatetimeIndex(["2024-01-01"])),
            ),
        }
        with patch("ingestion.dictionary.OUTPUT_DIR", str(tmp_path)):
            build_sidra_dictionaries(sidra)
            build_bcb_dictionaries(bcb)
            build_consolidated_dictionary()

        consolidated_path = tmp_path / "dictionary.json"
        assert consolidated_path.exists()
        entries = json.loads(consolidated_path.read_text())
        assert len(entries) == 2

        sidra_entry = next(e for e in entries if e["column"] == "pib__GDP")
        assert sidra_entry["file"] == "sidra/quarterly.csv"

        bcb_entry = next(e for e in entries if e["column"] == "selic")
        assert bcb_entry["file"] == "bcb/daily.csv"

    def test_empty_when_no_sources(self, tmp_path):
        with patch("ingestion.dictionary.OUTPUT_DIR", str(tmp_path)):
            build_consolidated_dictionary()
        consolidated_path = tmp_path / "dictionary.json"
        assert consolidated_path.exists()
        entries = json.loads(consolidated_path.read_text())
        assert entries == []


class TestBuildAll:
    def test_calls_all_builders_and_consolidates(self, tmp_path):
        with patch("ingestion.dictionary.OUTPUT_DIR", str(tmp_path)):
            build_all_dictionaries({}, {}, {}, {}, {}, {})
        consolidated = tmp_path / "dictionary.json"
        assert consolidated.exists()
        entries = json.loads(consolidated.read_text())
        assert entries == []
