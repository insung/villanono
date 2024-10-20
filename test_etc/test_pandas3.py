import os

import pandas as pd

__insight_describe_columns = [
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


def test(si, gu, dong, begin_year):
    df = pd.read_csv(os.path.join("data", "temp3", "서울특별시_연립다세대(매매).csv"))
    df2 = (
        df.query(
            f"시 == '{si}' & 구 == '{gu}' & 동 == '{dong}' & 계약일자 >= '{begin_year}0101'"
        )
        .groupby(["계약년월"], as_index=False)
        .agg(
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
    )

    df2.columns = __insight_describe_columns
    df2["평균(만원)"] = df2["평균(만원)"].round(2)

    print(df2.head())


test("서울특별시", "서대문구", "북가좌동", 2023)
