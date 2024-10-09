import pandas

from util import buysell_columns, buysell_describe_columns, get_output_file_path


def transfer_groupby_yyyyMM(
    temp_file_path: str, si: str, gu: str, dong: str, year: int
):
    selected_sizes = {
        "all": None,
        "under_20": "10평대",
        "under_30": "20평대",
        "under_40": "30평대",
        "over_40": "40평대 이상",
    }

    for key, value in selected_sizes.items():
        df = __file_to_dataframe(temp_file_path, value)
        df.to_csv(get_output_file_path(si, gu, dong, year, key), index=False)


def __file_to_dataframe(temp_file_path: str, selected_size: str | None):
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

    if selected_size is None:
        temp = df.groupby(["계약년월"], as_index=False).agg(aggregate)
    else:
        temp = (
            df.query(f"전용면적_그룹 == '{selected_size}'")
            .groupby(["계약년월"], as_index=False)
            .agg(aggregate)
        )
    temp.columns = buysell_describe_columns
    temp["평균(만원)"] = temp["평균(만원)"].round(2)
    return temp
