import os
import uuid

import pandas
from pandas import DataFrame, Series


def read_original_file(file_path: str, skiprows=15) -> DataFrame:
    with open(file_path, "r") as infile:
        content = infile.read()

    temp_outputfile_path = f"{uuid.uuid4()}.csv"

    with open(temp_outputfile_path, "w", encoding="utf-8") as outfile:
        outfile.write(content)

    df = pandas.read_csv(temp_outputfile_path, skiprows=skiprows)
    # df["보증금(만원)"] = df["보증금(만원)"].str.replace(",", "").astype(int)
    # df.to_csv("test.csv")
    os.remove(temp_outputfile_path)
    return df


def filter_by_yyyyMM(df: DataFrame, yyyyMM: int, rent_type: str = "전세") -> Series:
    filtered = df[(df["계약년월"] == yyyyMM) & (df["전월세구분"] == rent_type)]
    return filtered["보증금(만원)"].describe()


def groupby_yyyyMM(df: DataFrame):
    filtered = df[df["전월세구분"] == "전세"]
    selected = filtered[["계약년월", "보증금(만원)"]]
    return selected.groupby("계약년월")


buysell_columns = [
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

buysell_describe_columns = [
    "계약년월",
    "거래량(건)",
    "평균(만원)",
    "표준편차(만원)",
    "최소(만원)",
    "25%",
    "50%",
    "75%",
    "최대(만원)",
]

rent_columns = [
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


def makedirs_nested(base_path: str, dirs: list):
    if not dirs:
        return

    current_dir = os.path.join(base_path, dirs[0])

    if not os.path.exists(current_dir):
        os.makedirs(current_dir)

    makedirs_nested(current_dir, dirs[1:])


def split_division(groupby_division: set) -> DataFrame:
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


def get_data_file_path(
    begin_year: int, end_year: int, si: str, gu: str, dong: str
) -> str:
    return f"{begin_year}_{end_year}_{si} {gu} {dong}.csv"
