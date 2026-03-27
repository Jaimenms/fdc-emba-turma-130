"""Tests for ingestion.worldbank module."""

import pandas as pd
from unittest.mock import patch, MagicMock

from ingestion.worldbank import fetch_indicator


class TestFetchIndicator:
    @patch("ingestion.worldbank.requests.get")
    def test_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {"page": 1, "pages": 1, "total": 2},
            [
                {"date": "2023", "countryiso3code": "BRA", "value": 20.5},
                {"date": "2023", "countryiso3code": "AUS", "value": 25.3},
                {"date": "2022", "countryiso3code": "BRA", "value": 19.8},
                {"date": "2022", "countryiso3code": "AUS", "value": 24.1},
            ],
        ]
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        cfg = {"code": "NV.IND.TOTL.ZS", "name": "Industry GDP %", "description": "Test"}
        result = fetch_indicator("test", cfg, "BRA;AUS")

        assert result is not None
        assert len(result) == 2
        assert "test__BRA" in result.columns
        assert "test__AUS" in result.columns
        assert result.index.name == "year"

    @patch("ingestion.worldbank.requests.get")
    def test_null_values_excluded(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {"page": 1, "pages": 1, "total": 2},
            [
                {"date": "2023", "countryiso3code": "BRA", "value": None},
                {"date": "2022", "countryiso3code": "BRA", "value": 10.0},
            ],
        ]
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        cfg = {"code": "TEST", "name": "Test", "description": "Test"}
        result = fetch_indicator("test", cfg, "BRA")

        assert result is not None
        assert len(result) == 1

    @patch("ingestion.worldbank.requests.get")
    def test_api_error(self, mock_get):
        mock_get.side_effect = Exception("Network error")
        cfg = {"code": "TEST", "name": "Test", "description": "Test"}
        result = fetch_indicator("test", cfg, "BRA")
        assert result is None
