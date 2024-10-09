import pandas

from util import buysell_columns, buysell_describe_columns, get_output_file_path


def transfer_groupby_yyyyMM(
    temp_file_path: str, si: str, gu: str, dong: str, year: int
):
    df = pandas.read_csv(temp_file_path)
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

    under_20 = (
        df.query("전용면적_그룹 == '10평대 (33㎡미만)'")
        .groupby(["계약년월"], as_index=False)
        .agg(aggregate)
    )
    under_20.columns = buysell_describe_columns
    under_20["평균(만원)"] = under_20["평균(만원)"].round(2)

    under_30 = (
        df.query("전용면적_그룹 == '20평대 (66㎡미만)'")
        .groupby(["계약년월"], as_index=False)
        .agg(aggregate)
    )
    under_30.columns = buysell_describe_columns
    under_30["평균(만원)"] = under_30["평균(만원)"].round(2)

    under_40 = (
        df.query("전용면적_그룹 == '30평대 (99㎡미만)'")
        .groupby(["계약년월"], as_index=False)
        .agg(aggregate)
    )
    under_40.columns = buysell_describe_columns
    under_40["평균(만원)"] = under_40["평균(만원)"].round(2)

    over_40 = (
        df.query("전용면적_그룹 == '40평대 이상 (99㎡이상)'")
        .groupby(["계약년월"], as_index=False)
        .agg(aggregate)
    )
    over_40.columns = buysell_describe_columns
    over_40["평균(만원)"] = over_40["평균(만원)"].round(2)

    all_output_path = get_output_file_path(si, gu, dong, year)

    all_group.to_csv(all_output_path, index=False)
    # under_20.to_csv(path.join(dir, f"small_{year}.csv"), index=False)
    # under_30.to_csv(path.join(dir, f"medium_{year}.csv"), index=False)
    # under_40.to_csv(path.join(dir, f"large_{year}.csv"), index=False)
