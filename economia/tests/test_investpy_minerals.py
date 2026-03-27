"""Tests for ingestion.investpy_minerals module."""

import pandas as pd
from unittest.mock import patch, MagicMock

from ingestion.investpy_minerals import fetch_commodity


class TestFetchCommodity:
    @patch.dict("sys.modules", {"investpy": MagicMock()})
    def test_success(self):
        import sys
        mock_investpy = sys.modules["investpy"]
        mock_df = pd.DataFrame(
            {"Open": [2000], "High": [2050], "Low": [1990], "Close": [2030], "Volume": [100], "Currency": ["USD"]},
            index=pd.DatetimeIndex(["2024-01-02"], name="Date"),
        )
        mock_investpy.commodities.get_commodity_historical_data.return_value = mock_df

        cfg = {"commodity": "Gold", "name": "Ouro", "from_date": "01/01/2024", "to_date": "31/12/2024"}
        result = fetch_commodity("gold", cfg)

        assert result is not None
        assert len(result) == 1
        assert result.columns == ["gold"]
        assert result.iloc[0]["gold"] == 2030

    @patch.dict("sys.modules", {"investpy": MagicMock()})
    def test_commodity_not_found(self):
        import sys
        mock_investpy = sys.modules["investpy"]
        mock_investpy.commodities.get_commodity_historical_data.side_effect = RuntimeError("not found")

        cfg = {"commodity": "FakeOre", "name": "Fake"}
        result = fetch_commodity("fake", cfg)
        assert result is None

    @patch.dict("sys.modules", {"investpy": MagicMock()})
    def test_empty_result(self):
        import sys
        mock_investpy = sys.modules["investpy"]
        mock_investpy.commodities.get_commodity_historical_data.return_value = pd.DataFrame()

        cfg = {"commodity": "Gold", "name": "Ouro"}
        result = fetch_commodity("gold", cfg)
        assert result is None
