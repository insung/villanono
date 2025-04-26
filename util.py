import os
from genericpath import exists

import pandas
import requests
from pandas import DataFrame, Series


def filter_by_yyyyMM(df: DataFrame, yyyyMM: int, rent_type: str = "전세") -> Series:
    filtered = df[(df["계약년월"] == yyyyMM) & (df["전월세구분"] == rent_type)]
    return filtered["보증금(만원)"].describe()


def groupby_yyyyMM(df: DataFrame):
    filtered = df[df["전월세구분"] == "전세"]
    selected = filtered[["계약년월", "보증금(만원)"]]
    return selected.groupby("계약년월")


def makedirs_nested(base_path: str, dirs: list):
    if not dirs:
        return

    current_dir = os.path.join(base_path, dirs[0])

    if not os.path.exists(current_dir):
        os.makedirs(current_dir)

    makedirs_nested(current_dir, dirs[1:])


def to_dataframe_by_set(groupby_division: set) -> DataFrame:
    si = []
    gu = []
    dong = []
    for division in groupby_division:
        splits = division.split(" ")
        si.append(splits[0])
        gu.append(splits[1])
        dong.append(splits[2])

    df = pandas.DataFrame(list(zip(si, gu, dong)), columns=["시", "군", "구"])
    return df


def merge_division_data(groupby_divison_set: set, output_file_path: str) -> str:
    output_division_file_path = os.path.join(output_file_path, "division.csv")
    result_df = to_dataframe_by_set(groupby_divison_set)

    if exists(output_division_file_path):
        read_df = pandas.read_csv(output_division_file_path)
        result_df = result_df.astype(read_df.dtypes.to_dict())
        common_columns = ["시", "군", "구"]  # 공통 열 이름 리스트
        merged_df = read_df.merge(result_df, on=common_columns, how="outer")
        result_df = merged_df.drop_duplicates()

    result_df.to_csv(output_division_file_path, index=False)
    return output_division_file_path


def __get_output_file_path(
    year: int,
    si: str,
    gu: str,
    dong: str,
    selected_size: str,
    buy_or_rent: str = "buysell",
) -> str:
    temp = "매매" if buy_or_rent == "buysell" else "전세"
    result = os.path.join(
        "data", "output", si, gu, dong, selected_size, f"{year}_{temp}.csv"
    )
    return result


def get_dataframe_for_insight(
    begin_year: int,
    end_year: int,
    si: str,
    gu: str,
    dong: str,
    selected_size: str,
    buy_or_rent: str = "buysell",
) -> DataFrame:
    result = None

    for year in range(begin_year, end_year + 1):
        file_path = __get_output_file_path(
            year, si, gu, dong, selected_size, buy_or_rent
        )

        if not exists(file_path):
            continue

        df = pandas.read_csv(file_path)

        if result is None:
            result = df
        else:
            result = pandas.concat([result, df])

    return result


__division_df = pandas.read_csv(
    os.path.join("data", "output_divisions", "division.csv")
)


def read_divisions() -> dict:
    result = {}

    for si, gu, dong in zip(
        __division_df["시"], __division_df["군"], __division_df["구"]
    ):
        if si not in result:
            result[si] = {}
        if gu not in result[si]:
            result[si][gu] = []
        result[si][gu].append(dong)

    return result


def get_si_options() -> list:
    response = requests.get("http://localhost:5210/api/Location/Si")
    return response.json()


def get_gu_options(si: str = "서울특별시") -> list:
    response = requests.get(f"http://localhost:5210/api/Location/Si/{si}/Gu")
    gu_list: list = response.json()
    return sorted(gu_list)


def get_dong_options(si: str = "서울특별시", gu: str = "서대문구") -> list:
    response = requests.get(f"http://localhost:5210/api/Location/Si/{si}/Gu/{gu}/Dong")
    dong_list: list = response.json()
    return sorted(dong_list)


def makedir_if_not_exists(path: str):
    if not os.path.exists(path):
        os.makedirs(path)
