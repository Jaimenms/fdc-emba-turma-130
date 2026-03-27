"""Tests for ingestion.bcb module."""

import pandas as pd
import pytest
from unittest.mock import patch, MagicMock

from ingestion.bcb import fetch_series, save_bcb_results


class TestFetchSeries:
    @patch("ingestion.bcb.requests.get")
    def test_monthly_series(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"data": "01/01/2024", "valor": "11,75"},
            {"data": "01/02/2024", "valor": "11,25"},
        ]
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        cfg = {"code": 189, "name": "IGP-M", "frequency": "monthly", "unit": "%"}
        result = fetch_series("igpm", cfg)

        assert result is not None
        assert len(result) == 2
        assert result.columns == ["igpm"]
        assert result.iloc[0]["igpm"] == 11.75

    @patch("ingestion.bcb.requests.get")
    def test_api_error(self, mock_get):
        mock_get.side_effect = Exception("Connection error")
        cfg = {"code": 432, "name": "SELIC", "frequency": "daily", "unit": "%"}
        result = fetch_series("selic", cfg)
        assert result is None

    @patch("ingestion.bcb.requests.get")
    def test_empty_response(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        cfg = {"code": 189, "name": "IGP-M", "frequency": "monthly", "unit": "%"}
        result = fetch_series("igpm", cfg)
        assert result is None


class TestSaveBcbResults:
    def test_saves_by_frequency(self, tmp_path):
        daily_df = pd.DataFrame(
            {"selic": [11.75, 11.75]},
            index=pd.to_datetime(["2024-01-02", "2024-01-03"]),
        )
        daily_df.index.name = "date"
        monthly_df = pd.DataFrame(
            {"igpm": [0.5]},
            index=pd.to_datetime(["2024-01-01"]),
        )
        monthly_df.index.name = "date"

        results = {
            "selic": ({"frequency": "daily"}, daily_df),
            "igpm": ({"frequency": "monthly"}, monthly_df),
        }

        with patch("ingestion.bcb.OUTPUT_DIR", str(tmp_path)):
            save_bcb_results(results)

        assert (tmp_path / "bcb" / "daily.csv").exists()
        assert (tmp_path / "bcb" / "monthly.csv").exists()
