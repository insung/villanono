import os
import uuid

import pandas
from pandas import DataFrame, Series


def read_original_file(file_path: str) -> DataFrame:
    with open(file_path, "r") as infile:
        content = infile.read()

    temp_outputfile_path = f"{uuid.uuid4()}.csv"

    with open(temp_outputfile_path, "w", encoding="utf-8") as outfile:
        outfile.write(content)

    df = pandas.read_csv(temp_outputfile_path, skiprows=15)
    df["보증금(만원)"] = df["보증금(만원)"].str.replace(",", "").astype(int)
    # df.to_csv("test.csv")
    os.remove(temp_outputfile_path)
    return df


def filter_by_yyyyMM(df: DataFrame, yyyyMM: int, rent_type: str = "전세") -> Series:
    filtered = df[(df["계약년월"] == yyyyMM) & (df["전월세구분"] == rent_type)]
    return filtered["보증금(만원)"].describe()
