import unittest
from unittest.mock import patch

import pandas as pd

from etl.buysell_etl import extract_division_data


class TestExtractDivisionData(unittest.TestCase):
    @patch("util.read_original_file")
    @patch("util.split_division")
    @patch("os.path.join")
    def test_extract_division_data(
        self, mock_path_join, mock_split_division, mock_read_original_file
    ):
        # Mock data
        mock_data = {
            "NO": [1],
            "시군구": ["서울특별시 서대문구 북가좌동"],
            "번지": ["313-19"],
            "본번": [313],
            "부번": [19],
            "건물명": ["신안휴먼타운"],
            "전용면적(㎡)": [41.35],
            "대지권면적(㎡)": [26.32],
            "계약년월": [202408],
            "계약일": [25],
            "거래금액(만원)": ["27,600"],
            "층": [4],
            "매수자": ["개인"],
            "매도자": ["개인"],
            "건축년도": [2019],
            "도로명": ["거북골로20길 43-13"],
            "해제사유발생일": ["-"],
            "거래유형": ["직거래"],
            "중개사소재지": ["="],
            "등기일자": ["-"],
        }

        # Setup mock return values
        mock_read_original_file.return_value = pd.DataFrame(mock_data)
        mock_split_division.return_value = pd.DataFrame(mock_data)
        mock_path_join.side_effect = lambda *args: "/".join(args)

        # Call the function
        year = 2023
        result = extract_division_data(year)

        # Assertions
        mock_read_original_file.assert_called_once_with(
            "/data/original/매매/2023_연립다세대(매매).csv"
        )

        mock_split_division.assert_called_once_with(set(mock_data["시군구"]))
        self.assertEqual(result, "/your/temp/division/path/2023_division.csv")

        # Check if the file was saved correctly
        saved_df = pd.read_csv(result)
        pd.testing.assert_frame_equal(saved_df, pd.DataFrame(mock_data))
