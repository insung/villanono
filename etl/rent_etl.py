import os
from os import path

import pandas

from util import (
    read_original_file,
    size_labels,
    size_ranges,
    temp_output_path,
    transfer_groupby_yyyyMM,
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


__rent_columns = [
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


def extract_original_rent_data(
    si: str,
    gu: str,
    dong: str,
    year: int,
    data_file_path: str = "data\\original\\전월세\\2023_연립다세대(전월세).csv",
):
    original_data_list = []
    df1 = read_original_file(data_file_path)
    df2 = df1.query(f"전월세구분 == '전세' & 시군구 == '{si} {gu} {dong}'")
    df2["보증금(만원)"] = df2["보증금(만원)"].str.replace(",", "").astype(int)
    df2.loc[:, "계약일자"] = df2["계약년월"].astype(str) + df2["계약일"].astype(
        str
    ).str.zfill(2)
    df2["계약일자"] = pandas.to_datetime(df2["계약일자"], format="%Y%m%d")

    col_name = df2.columns.values[7]  # 전용면적

    df2["전용면적_그룹"] = pandas.cut(
        df2[col_name], bins=size_ranges, labels=size_labels, right=False
    )
    original_data_list.append(df2)

    dir = path.join(temp_output_path, si, gu, dong)
    temp_file_path = path.join(dir, f"{year}_전세.csv")

    if not os.path.exists(dir):
        os.makedirs(dir)

    pandas.concat(original_data_list).to_csv(temp_file_path)
    return temp_file_path


def run():
    year = 2024
    si = "서울특별시"
    gu = "서대문구"
    dong = "북가좌동"

    # sigudong = read_divisions()

    temp_file_path = extract_original_rent_data(si, gu, dong, year)
    transfer_groupby_yyyyMM(temp_file_path, si, gu, dong, year, __rent_columns)


run()
