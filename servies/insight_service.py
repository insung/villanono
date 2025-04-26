import os
from datetime import datetime

import pandas as pd

from servies.insight_query import get_insight_query


def __get_insight_data(
    file_path: str,
    begin_date: datetime,
    selected_si: str,
    selected_gu: str,
    selected_dong: str | None,
    selected_built_year: datetime | None,
    selected_size: str | None,
) -> pd.DataFrame:
    query = get_insight_query(
        begin_date,
        selected_si,
        selected_gu,
        selected_dong,
        selected_built_year,
        selected_size,
    )

    begin_yyyyMM = int(begin_date.strftime("%Y%m"))

    read_df = pd.read_csv(file_path)
    queried_df = read_df.query(query)

    df = queried_df.groupby(["계약년월"], as_index=False).agg(
        {
            "거래금액(만원)": [
                "count",
                "mean",
                "std",
                "min",
                lambda x: x.quantile(0.25),
                "median",
                lambda x: x.quantile(0.75),
                "max",
            ]
        }
    )

    df.columns = [
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

    df["평균(만원)"] = df["평균(만원)"].round(2)
    df = df.query(f"계약년월 > {begin_yyyyMM}")
    df["계약년월"] = pd.to_datetime(df["계약년월"], format="%Y%m")

    return df


def load_buysell_data(
    begin_date: datetime,
    selected_si: str,
    selected_gu: str,
    selected_dong: str | None,
    selected_built_year: datetime | None,
    selected_size: str | None,
) -> pd.DataFrame:
    file_path_buysell = os.path.join(
        "data",
        "latest",
        "서울특별시",
        f"{selected_gu}_연립다세대(매매).csv",
    )
    df_buysell = __get_insight_data(
        file_path_buysell,
        begin_date,
        selected_si,
        selected_gu,
        selected_dong,
        selected_built_year,
        selected_size,
    )
    return df_buysell


def load_rent_data(
    begin_date: datetime,
    selected_si: str,
    selected_gu: str,
    selected_dong: str | None,
    selected_built_year: datetime | None,
    selected_size: str | None,
) -> pd.DataFrame:
    file_path_rent = os.path.join(
        "data",
        "latest",
        "서울특별시",
        f"{selected_gu}_연립다세대(전월세).csv",
    )
    df_rent = __get_insight_data(
        file_path_rent,
        begin_date,
        selected_si,
        selected_gu,
        selected_dong,
        selected_built_year,
        selected_size,
    )
    return df_rent


def load_buysell_rent_rate_data(
    df_buysell: pd.DataFrame, df_rent: pd.DataFrame
) -> pd.DataFrame:
    df_merged = pd.merge(
        df_buysell, df_rent, on="계약년월", suffixes=("_매매", "_전세")
    )

    # 전세가율 계산
    df_merged["전세가율(%)"] = (
        df_merged["평균(만원)_전세"] / df_merged["평균(만원)_매매"]
    ) * 100

    df_merged = df_merged[
        ["계약년월", "평균(만원)_매매", "평균(만원)_전세", "전세가율(%)"]
    ]

    return df_merged


def set_columns_round(df: pd.DataFrame):
    df[
        [
            "평균(만원)",
            "표준편차(만원)",
            "최소(만원)",
            "25%",
            "50%",
            "75%",
            "최대(만원)",
        ]
    ] = df[
        [
            "평균(만원)",
            "표준편차(만원)",
            "최소(만원)",
            "25%",
            "50%",
            "75%",
            "최대(만원)",
        ]
    ].round(-2)

    df["계약년월"] = df["계약년월"].dt.date


def set_columns_round_rate(df: pd.DataFrame):
    df[["평균(만원)_전세", "평균(만원)_매매"]] = df[
        ["평균(만원)_전세", "평균(만원)_매매"]
    ].round(-2)

    df["전세가율(%)"] = df["전세가율(%)"].round(0)
    df["계약년월"] = df["계약년월"].dt.date
