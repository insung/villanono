import os
import uuid
from genericpath import exists

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


def get_output_file_path(
    si: str, gu: str, dong: str, year: int, selected_size: str
) -> str:
    dir = os.path.join("data", "output", si, gu, dong, selected_size)
    if not os.path.exists(dir):
        os.makedirs(dir)

    return os.path.join(dir, f"{year}.csv")


def get_dataframe_for_insight(
    begin_year: int, end_year: int, si: str, gu: str, dong: str, selected_size: str
) -> DataFrame:
    result = None

    for year in range(begin_year, end_year + 1):
        file_path = get_output_file_path(si, gu, dong, year, selected_size)

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
    return __division_df["시"].unique().tolist()


def get_gu_options(si: str = "서울특별시") -> list:
    return (
        __division_df.query(f"시 == '{si}'")
        .sort_values(by="군", ascending=True)["군"]
        .unique()
        .tolist()
    )


def get_dong_options(gu: str = "서대문구") -> list:
    return (
        __division_df.query(f"군 == '{gu}'")
        .sort_values(by="구", ascending=True)["구"]
        .unique()
        .tolist()
    )
