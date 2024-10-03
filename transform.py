import pandas

from util import buysell_columns, buysell_describe_columns

# df_division = pandas.read_csv(temp_division_file)
# print(df_division.head())

df = pandas.read_csv("data\\temp\\2022_2024_서울특별시 서대문구 북가좌동.csv")
df.columns = buysell_columns

aggregate = {
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

# print(df.head())
# temp1 = df.query("전용면적 < 50")
all_group = df.groupby(["계약년월"], as_index=False).agg(aggregate)
all_group.columns = buysell_describe_columns
all_group["평균(만원)"] = all_group["평균(만원)"].round(2)


small_group = (
    df.query("전용면적_그룹 == '소형(60미만)'")
    .groupby(["계약년월"], as_index=False)
    .agg(aggregate)
)
small_group.columns = buysell_describe_columns
small_group["평균(만원)"] = small_group["평균(만원)"].round(2)


medium_group = (
    df.query("전용면적_그룹 == '중형(80미만)'")
    .groupby(["계약년월"], as_index=False)
    .agg(aggregate)
)
medium_group.columns = buysell_describe_columns
medium_group["평균(만원)"] = medium_group["평균(만원)"].round(2)

large_group = (
    df.query("전용면적_그룹 == '대형(80이상)'")
    .groupby(["계약년월"], as_index=False)
    .agg(aggregate)
)
large_group.columns = buysell_describe_columns
large_group["평균(만원)"] = large_group["평균(만원)"].round(2)

all_group.to_csv(
    "data\\temp2\\all_2022_2024_서울특별시 서대문구 북가좌동.csv", index=False
)
small_group.to_csv(
    "data\\temp2\\small_2022_2024_서울특별시 서대문구 북가좌동.csv", index=False
)
medium_group.to_csv(
    "data\\temp2\\medium_2022_2024_서울특별시 서대문구 북가좌동.csv", index=False
)
large_group.to_csv(
    "data\\temp2\\large_2022_2024_서울특별시 서대문구 북가좌동.csv", index=False
)
