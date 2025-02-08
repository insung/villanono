import os
import uuid
from genericpath import exists
from typing import Literal

import pandas

from util import makedir_if_not_exists, read_divisions

__si = "서울특별시"
__readable_path = os.path.join("data", "original_to_csv", __si)
__size_ranges = [0, 33, 66, 99, 1653]
__size_labels = [
    "10평대",
    "20평대",
    "30평대",
    "40평대 이상",
]


sigudong = read_divisions()


def concat_output_data(
    df: pandas.DataFrame,
    year: int,
    file_name: str = Literal["_연립다세대(매매).csv", "_연립다세대(전월세).csv"],
):
    for si_items in sigudong.items():
        for gu_dict in si_items[1].items():
            gu = gu_dict[0]

            result = df.query(f"구 == '{gu}'")
            result_file_path = os.path.join("data", "temp3", __si, f"{gu}{file_name}")

            print("processing", year, gu)

            if exists(result_file_path):
                old = pandas.read_csv(result_file_path)
                result = pandas.concat([old, result])

                result.to_csv(
                    result_file_path,
                    index=False,
                )
            else:
                result.to_csv(
                    result_file_path,
                    index=False,
                )


def delete_and_merge(
    df: pandas.DataFrame,
    year: int,
    file_name: str = Literal["_연립다세대(매매).csv", "_연립다세대(전월세).csv"],
):
    for si_items in sigudong.items():
        for gu_dict in si_items[1].items():
            gu = gu_dict[0]

            result = df.query(f"구 == '{gu}'")
            original_file_path = os.path.join("data", "temp3", __si, f"{gu}{file_name}")
            original_df = pandas.read_csv(original_file_path)
            filtered_df = original_df[original_df["계약년월"] <= int(f"{year}01")]

            print("processing", year, gu)

            result_file_path = os.path.join("data", "temp4", __si, f"{gu}{file_name}")
            concat_df = pandas.concat([filtered_df, result])
            concat_df.to_csv(result_file_path, index=False)


def run_original_to_readable(
    year: int,
    file_name: str = Literal["_연립다세대(매매).csv", "_연립다세대(전월세).csv"],
):
    makedir_if_not_exists(__readable_path)
    file_path = f"{year}{file_name}"

    with open(os.path.join("data", "original", __si, file_path), "r") as infile:
        content = infile.read()

    temp_outputfile_path = os.path.join("data", "temp2", f"{uuid.uuid4()}.csv")

    with open(temp_outputfile_path, "w", encoding="utf-8") as outfile:
        outfile.write(content)

    df = pandas.read_csv(temp_outputfile_path, skiprows=15, low_memory=False)
    os.remove(temp_outputfile_path)
    output_file_path = os.path.join(__readable_path, file_path)
    if exists(output_file_path):
        os.remove(output_file_path)

    df.to_csv(output_file_path, index=False)


def run_readable_to_buysell(
    year: int, file_name: str = Literal["_연립다세대(매매).csv"]
) -> pandas.DataFrame:
    file_path = f"{year}{file_name}"

    df = pandas.read_csv(os.path.join(__readable_path, file_path))

    df["거래금액(만원)"] = df["거래금액(만원)"].str.replace(",", "").astype(int)
    df.loc[:, "계약일자"] = df["계약년월"].astype(str) + df["계약일"].astype(
        str
    ).str.zfill(2)
    df["계약일자"] = pandas.to_datetime(df["계약일자"], format="%Y%m%d")

    df.columns = [
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
    ]

    df[["시", "구", "동"]] = df["시군구"].str.split(" ", expand=True)
    df = df.drop(columns=["NO", "시군구"])

    cols = ["시", "구", "동"] + [
        col for col in df.columns if col not in ["시", "구", "동"]
    ]

    # 컬럼 순서 변경
    df = df[cols]

    df["전용면적_그룹"] = pandas.cut(
        df["전용면적"],
        bins=__size_ranges,
        labels=__size_labels,
        right=False,
    )

    return df


def run_readable_to_rent(
    year: int, file_name: str = Literal["_연립다세대(전월세).csv"]
) -> pandas.DataFrame:
    file_path = f"{year}{file_name}"

    original_df = pandas.read_csv(os.path.join(__readable_path, file_path))

    df = original_df.query("전월세구분 == '전세'")
    df["거래금액(만원)"] = df["보증금(만원)"].str.replace(",", "").astype(int)
    df.loc[:, "계약일자"] = df["계약년월"].astype(str) + df["계약일"].astype(
        str
    ).str.zfill(2)
    df["계약일자"] = pandas.to_datetime(df["계약일자"], format="%Y%m%d")

    df.columns = [
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
        "거래금액(만원)",
        "계약일자",
    ]

    df[["시", "구", "동"]] = df["시군구"].str.split(" ", expand=True)
    df = df.drop(columns=["NO", "시군구"])

    cols = ["시", "구", "동"] + [
        col for col in df.columns if col not in ["시", "구", "동"]
    ]

    # 컬럼 순서 변경
    df = df[cols]

    df["전용면적_그룹"] = pandas.cut(
        df["전용면적"],
        bins=__size_ranges,
        labels=__size_labels,
        right=False,
    )

    return df


file_name = "_연립다세대(전월세).csv"
# file_name = "_연립다세대(매매).csv"

# run_original_to_readable(2024, file_name) # 새로운 공공데이터 파일을 읽어야 한다면

df = run_readable_to_rent(2024, file_name)
# df = run_readable_to_buysell(2024, file_name)

# concat_output_data(df, 2024, file_name) # original 파일에 2024년도를 붙이고 싶다면
delete_and_merge(df, 2024, file_name)  # 2024년도만 다시 만들고 싶다면
