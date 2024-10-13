from os import path

from etl.insight_etl_abc import (
    InsightETLABC,
)
from util import (
    makedir_if_not_exists,
)

__rent_columns2 = [
    "NO",
    "시군구",
    "번지",
    "본번",
    "부번",
    "건물명",
    "전월세구분",
    "전용면적",
    "계약년월",
    "계약일",
    "보증금(만원)",
    "월세금(만원)",
    "층",
    "건축년도",
    "도로명",
    "계약기간",
    "계약구분",
    "갱신요구권 사용",
    "종전계약 보증금(만원)",
    "종전계약 월세(만원)",
    "주택유형",
]


class InsightRentETL(InsightETLABC):
    def __init__(self, si: str, gu: str, dong: str, year: int):
        self.si = si
        self.gu = gu
        self.dong = dong
        self.year = year
        makedir_if_not_exists(self.get_dir_data_temp())

    def get_columns(self) -> list[str]:
        return [
            "Unnamed: 0",
            "NO",
            "시군구",
            "번지",
            "본번",
            "부번",
            "건물명",
            "전월세구분",
            "전용면적(㎡)",
            "계약년월",
            "계약일",
            "거래금액(만원)",
            "월세금(만원)",
            "층",
            "건축년도",
            "도로명",
            "계약기간",
            "계약구분",
            "갱신요구권 사용",
            "종전계약 보증금(만원)",
            "종전계약 월세(만원)",
            "주택유형",
            "계약일자",
            "전용면적_그룹",
        ]

    def get_filename(self) -> str:
        return f"{self.year}_전세.csv"

    def get_path_data_original(self) -> str:
        return path.join(
            self.dir_data_original, self.si, f"{self.year}_연립다세대(전월세).csv"
        )

    def get_dir_data_temp(self) -> str:
        return path.join(self.dir_data_temp, self.si, self.gu, self.dong)

    def get_dir_data_output(self) -> str:
        return path.join(self.dir_data_output, self.si, self.gu, self.dong)

    def get_extract_query(self) -> str:
        return f"전월세구분 == '전세' & 시군구 == '{self.si} {self.gu} {self.dong}'"

    def get_extract_sales_column(self) -> str:
        return "보증금(만원)"

    def get_extract_size_column_index(self) -> int:
        return 7
