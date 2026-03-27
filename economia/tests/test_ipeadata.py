"""Tests for ingestion.ipeadata module."""

import pandas as pd
from unittest.mock import patch, MagicMock

from ingestion.ipeadata import fetch_series


class TestFetchSeries:
    @patch("ingestion.ipeadata.requests.get")
    def test_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "value": [
                {"SERCODIGO": "TEST", "VALDATA": "2024-01-01T00:00:00-03:00", "VALVALOR": 100.5},
                {"SERCODIGO": "TEST", "VALDATA": "2024-02-01T00:00:00-03:00", "VALVALOR": 101.3},
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        cfg = {"code": "TEST_CODE", "name": "Test", "frequency": "monthly", "unit": "pts"}
        result = fetch_series("test", cfg)

        assert result is not None
        assert len(result) == 2
        assert result.columns == ["test"]

    @patch("ingestion.ipeadata.requests.get")
    def test_null_values_filtered(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "value": [
                {"SERCODIGO": "T", "VALDATA": "2024-01-01T00:00:00-03:00", "VALVALOR": 100.5},
                {"SERCODIGO": "T", "VALDATA": "2024-02-01T00:00:00-03:00", "VALVALOR": None},
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        cfg = {"code": "TEST", "name": "Test", "frequency": "monthly", "unit": "pts"}
        result = fetch_series("test", cfg)

        assert result is not None
        assert len(result) == 1

    @patch("ingestion.ipeadata.requests.get")
    def test_empty_response(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"value": []}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        cfg = {"code": "TEST", "name": "Test", "frequency": "monthly", "unit": "pts"}
        result = fetch_series("test", cfg)
        assert result is None
