from os import path

from etl.insight_etl_abc import (
    InsightETLABC,
)
from util import (
    makedir_if_not_exists,
)

__output_division_path = path.join("data", "output_divisions")


class InsightBuySellETL(InsightETLABC):
    si: str
    gu: str
    dong: str
    year: int

    def __init__(self, si: str, gu: str, dong: str, year: int):
        self.si = si
        self.gu = gu
        self.dong = dong
        self.year = year
        makedir_if_not_exists(self.get_dir_data_temp())

    def get_columns(self) -> list[str]:
        return [
            "row_index",
            "NO",
            "시군구",
            "번지",
            "본번",
            "부번",
            "건물명",
            "전용면적",
            "대지권면적",
            "계약년월",
            "계약일",
            "거래금액(만원)",
            "층",
            "매수자",
            "매도자",
            "건축년도",
            "도로명",
            "해제사유발생일",
            "거래유형",
            "중개사소재지",
            "등기일자",
            "계약일자",
            "전용면적_그룹",
        ]

    def get_filename(self) -> str:
        return f"{self.year}_매매.csv"

    def get_path_data_original(self) -> str:
        return path.join(
            self.dir_data_original, self.si, f"{self.year}_연립다세대(매매).csv"
        )

    def get_dir_data_temp(self) -> str:
        return path.join(self.dir_data_temp, self.si, self.gu, self.dong)

    def get_dir_data_output(self) -> str:
        return path.join(self.dir_data_output, self.si, self.gu, self.dong)

    def get_extract_query(self) -> str:
        return f"시군구 == '{self.si} {self.gu} {self.dong}'"

    def get_extract_sales_column(self) -> str:
        return "거래금액(만원)"

    def get_extract_size_column_index(self) -> int:
        return 6


# def extract_division_data(
#     data_file_path: str, output_file_path: str, column: str = "시군구"
# ) -> str:
#     groupby_divison_set = set()
#     original_data_df = read_original_file(data_file_path)
#     groupby_divison = original_data_df[column].unique().tolist()
#     groupby_divison_set.update(groupby_divison)
#     output_file_path = merge_division_data(groupby_divison, output_file_path)
#     return output_file_path
