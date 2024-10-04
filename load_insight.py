import os

import pandas as pd
from pandas import DataFrame

from util import get_data_file_path

current_path = os.getcwd()


def get_dataframe_for_insight(
    begin_year: int, end_year: int, si: str, gu: str, dong: str, selected_size: str
) -> DataFrame:
    file_path_prefix = "all"
    if selected_size == "소형(60㎡미만)":
        file_path_prefix = "small]"
    elif selected_size == "중형(80㎡미만)":
        file_path_prefix = "medium"
    elif selected_size == "대형(80㎡이상)":
        file_path_prefix = "large"

    file_path_suffix = get_data_file_path(begin_year, end_year, si, gu, dong)

    file_path = os.path.join(
        current_path,
        "data",
        "temp2",
        f"{file_path_prefix}_{file_path_suffix}",
    )
    return pd.read_csv(file_path)
