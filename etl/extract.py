import os
from os import path

import pandas

from util import merge_division_data, read_original_file

__temp_output_path = path.join("data", "temp")


def extract_original_data(
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

    size_ranges = [0, 33, 66, 99, 1653]
    size_labels = [
        "10평대 (33㎡미만)",
        "20평대 (66㎡미만)",
        "30평대 (99㎡미만)",
        "40평대 이상 (99㎡이상)",
    ]

    df2["전용면적_그룹"] = pandas.cut(
        df2[col_name], bins=size_ranges, labels=size_labels, right=False
    )
    original_data_list.append(df2)

    dir = path.join(__temp_output_path, si, gu, dong)
    temp_file_path = path.join(dir, f"{year}.csv")

    if not os.path.exists(dir):
        os.makedirs(dir)

    pandas.concat(original_data_list).to_csv(temp_file_path)
    return temp_file_path


def extract_division_data(
    data_file_path: str, output_file_path: str, column: str = "시군구"
) -> str:
    groupby_divison_set = set()
    original_data_df = read_original_file(data_file_path)
    groupby_divison = original_data_df[column].unique().tolist()
    groupby_divison_set.update(groupby_divison)
    output_file_path = merge_division_data(groupby_divison, output_file_path)
    return output_file_path
