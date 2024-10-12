import os
from os import path

import pandas

from util import (
    merge_division_data,
    read_divisions,
    read_original_file,
    size_labels,
    size_ranges,
    temp_output_path,
    transfer_groupby_yyyyMM,
)

__original_data_path = path.join("data", "original", "매매")
__output_division_path = path.join("data", "output_divisions")

__buysell_columns = [
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


def extract_division_data(
    data_file_path: str, output_file_path: str, column: str = "시군구"
) -> str:
    groupby_divison_set = set()
    original_data_df = read_original_file(data_file_path)
    groupby_divison = original_data_df[column].unique().tolist()
    groupby_divison_set.update(groupby_divison)
    output_file_path = merge_division_data(groupby_divison, output_file_path)
    return output_file_path


def extract_original_buysell_data(
    data_file_path: str,
    year: int,
    si: str,
    gu: str,
    dong: str,
) -> str:
    original_data_list = []
    df1 = read_original_file(data_file_path)
    df2 = df1.query(f"시군구 == '{si} {gu} {dong}'")

    df2["거래금액(만원)"] = df2["거래금액(만원)"].str.replace(",", "").astype(int)

    df2.loc[:, "계약일자"] = df2["계약년월"].astype(str) + df2["계약일"].astype(
        str
    ).str.zfill(2)
    df2["계약일자"] = pandas.to_datetime(df2["계약일자"], format="%Y%m%d")

    col_name = df2.columns.values[6]  # 전용면적

    df2["전용면적_그룹"] = pandas.cut(
        df2[col_name], bins=size_ranges, labels=size_labels, right=False
    )
    original_data_list.append(df2)

    dir = path.join(temp_output_path, si, gu, dong)
    temp_file_path = path.join(dir, f"{year}.csv")

    if not os.path.exists(dir):
        os.makedirs(dir)

    pandas.concat(original_data_list).to_csv(temp_file_path)
    return temp_file_path


def run():
    sigudong = read_divisions()

    for year in range(2006, 2024 + 1):
        data_file_path = path.join(__original_data_path, f"{year}_연립다세대(매매).csv")
        # extract_division_data(data_file_path, __output_division_path)

        for si_items in sigudong.items():
            for gu_dict in si_items[1].items():
                for dong in gu_dict[1]:
                    if (
                        si_items == "서울특별시"
                        and gu_dict == "서대문구"
                        and dong == "북가좌동"
                    ):
                        continue
                    else:
                        si = si_items[0]
                        gu = gu_dict[0]
                        temp_file_path = extract_original_buysell_data(
                            data_file_path, year, si, gu, dong
                        )
                        transfer_groupby_yyyyMM(
                            temp_file_path, si, gu, dong, year, __buysell_columns
                        )
