from os import path

from etl.extract import extract_original_data
from etl.transform import transfer_groupby_yyyyMM
from util import read_divisions

__original_data_path = path.join("data", "original", "매매")
__output_division_path = path.join("data", "output_divisions")

sigudong = read_divisions()


for year in range(2006, 2024 + 1):
    data_file_path = path.join(__original_data_path, f"{year}_연립다세대(매매).csv")
    # extract_division_data(data_file_path, __output_division_path)

    for si_items in sigudong.items():
        for gu_dict in si_items[1].items():
            for dong in gu_dict[1]:
                if (
                    si_items == "서울특별시"
                    and gu_dict == "서대문구"
                    and dong == "북가좌동"
                ):
                    continue
                else:
                    si = si_items[0]
                    gu = gu_dict[0]
                    temp_file_path = extract_original_data(
                        data_file_path, year, si, gu, dong
                    )
                    transfer_groupby_yyyyMM(temp_file_path, si, gu, dong, year)
