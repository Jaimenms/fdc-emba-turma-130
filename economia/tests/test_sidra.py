"""Tests for ingestion.sidra module."""

import pandas as pd
import pytest
from unittest.mock import patch, MagicMock

from ingestion.sidra import fetch_table, parse_period, process_table


class TestParsePeriod:
    def test_monthly(self):
        assert parse_period("202401", "monthly") == pd.Timestamp("2024-01-01")

    def test_monthly_december(self):
        assert parse_period("202312", "monthly") == pd.Timestamp("2023-12-01")

    def test_quarterly_q1(self):
        assert parse_period("202401", "quarterly") == pd.Timestamp("2024-01-01")

    def test_quarterly_q3(self):
        assert parse_period("202403", "quarterly") == pd.Timestamp("2024-07-01")

    def test_quarterly_q4(self):
        assert parse_period("202404", "quarterly") == pd.Timestamp("2024-10-01")

    def test_annual(self):
        assert parse_period("2023", "annual") == pd.Timestamp("2023-01-01")

    def test_invalid(self):
        assert pd.isna(parse_period("abc", "monthly"))

    def test_none(self):
        assert pd.isna(parse_period(None, "monthly"))

    def test_empty(self):
        assert pd.isna(parse_period("", "monthly"))


class TestFetchTable:
    @patch("ingestion.sidra.sidrapy.get_table")
    def test_success(self, mock_get):
        mock_get.return_value = pd.DataFrame({
            "D2C": ["Período (Código)", "202401"],
            "V": ["Valor", "100.5"],
            "D3N": ["Variável", "Test var"],
        })
        cfg = {
            "table_code": "1620",
            "territorial_level": "1",
            "ibge_territorial_code": "all",
            "period": "all",
            "variable": "583",
            "classifications": {},
        }
        result = fetch_table("test", cfg)
        assert result is not None
        assert len(result) == 1  # header row removed

    @patch("ingestion.sidra.sidrapy.get_table")
    def test_api_error(self, mock_get):
        mock_get.side_effect = ValueError("API error")
        cfg = {
            "table_code": "1620",
            "territorial_level": "1",
            "ibge_territorial_code": "all",
            "period": "all",
            "variable": "583",
            "classifications": {},
        }
        result = fetch_table("test", cfg)
        assert result is None

    @patch("ingestion.sidra.sidrapy.get_table")
    def test_empty_response(self, mock_get):
        mock_get.return_value = pd.DataFrame()
        cfg = {
            "table_code": "1620",
            "territorial_level": "1",
            "ibge_territorial_code": "all",
            "period": "all",
        }
        result = fetch_table("test", cfg)
        assert result is None


class TestProcessTable:
    def test_basic_processing(self):
        raw_df = pd.DataFrame({
            "D2C": ["202401", "202402"],
            "V": ["100.5", "101.3"],
            "D3N": ["GDP Index", "GDP Index"],
        })
        cfg = {"frequency": "monthly"}
        result = process_table("test", cfg, raw_df)
        assert result is not None
        assert len(result) == 2
        assert result.index.name == "date"

    def test_missing_columns(self):
        raw_df = pd.DataFrame({"X": [1], "Y": [2]})
        cfg = {"frequency": "monthly"}
        result = process_table("test", cfg, raw_df)
        assert result is None

    def test_handles_missing_values(self):
        raw_df = pd.DataFrame({
            "D2C": ["202401", "202402", "202403"],
            "V": ["100.5", "...", "-"],
            "D3N": ["X", "X", "X"],
        })
        cfg = {"frequency": "monthly"}
        result = process_table("test", cfg, raw_df)
        assert result is not None
        # "..." and "-" become NaN; pivot_table keeps only rows with at least one non-NaN
        assert len(result) == 1
        assert result.iloc[0].values[0] == 100.5

    def test_pivot_multiple_indicators(self):
        raw_df = pd.DataFrame({
            "D2C": ["202401", "202401"],
            "V": ["10", "20"],
            "D3N": ["Var A", "Var B"],
        })
        cfg = {"frequency": "monthly"}
        result = process_table("test", cfg, raw_df)
        assert result is not None
        assert len(result.columns) == 2
