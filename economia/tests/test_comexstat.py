"""Tests for ingestion.comexstat module."""

import pandas as pd
from unittest.mock import patch, MagicMock

from ingestion.comexstat import _download_year


class TestDownloadYear:
    @patch("ingestion.comexstat.requests.get")
    def test_parses_csv(self, mock_get):
        csv_content = (
            '"CO_ANO";"CO_MES";"CO_NCM";"CO_UNID";"CO_PAIS";"SG_UF_NCM";"CO_VIA";"CO_URF";"QT_ESTAT";"KG_LIQUIDO";"VL_FOB"\n'
            '"2024";"01";"26011100";"10";"160";"MG";"01";"0817800";"1000";"5000000";"2500000"\n'
            '"2024";"01";"26011200";"10";"160";"PA";"01";"0417800";"500";"3000000";"1500000"\n'
        )
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = csv_content
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        df = _download_year("export", 2024)
        assert df is not None
        assert len(df) == 2
        assert "SH4" in df.columns
        assert "SH2" in df.columns
        assert df.iloc[0]["SH4"] == "2601"
        assert df.iloc[0]["SH2"] == "26"
        assert df.iloc[0]["VL_FOB"] == 2500000

    @patch("ingestion.comexstat.requests.get")
    def test_handles_error(self, mock_get):
        mock_get.side_effect = Exception("Network error")
        df = _download_year("export", 2024)
        assert df is None
