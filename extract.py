import pandas

from util import read_original_file, split_division

# splits = "서울특별시 성북구 정릉동".split(" ")
# makedirs_nested("data/division", splits)


def extract_original_data(
    begin_year: int,
    end_year: int,
    selected_division: str = "서울특별시 서대문구 북가좌동",
):
    original_data_list = []

    for i in range(begin_year, end_year + 1):
        df1 = read_original_file(f"data\\original\\매매\\{i}_연립다세대(매매).csv")
        df2 = df1.query(f"시군구 == '{selected_division}'")

        df2["거래금액(만원)"] = df2["거래금액(만원)"].str.replace(",", "").astype(int)

        df2.loc[:, "계약일자"] = df2["계약년월"].astype(str) + df2["계약일"].astype(
            str
        ).str.zfill(2)
        df2["계약일자"] = pandas.to_datetime(df2["계약일자"], format="%Y%m%d")

        col_name = df2.columns.values[6]

        size_ranges = [0, 60, 80, 3000]
        size_labels = ["소형(60미만)", "중형(80미만)", "대형(80이상)"]

        df2["전용면적_그룹"] = pandas.cut(
            df2[col_name], bins=size_ranges, labels=size_labels, right=False
        )
        original_data_list.append(df2)

    temp_file = f"data\\temp\\{begin_year}_{end_year}_{selected_division}.csv"
    pandas.concat(original_data_list).to_csv(temp_file)


def extract_division_data(
    begin_year: int, end_year: int, temp_division_file: str = "data\\temp\\division.csv"
):
    groupby_divison_list = set()

    for i in range(begin_year, end_year + 1):
        df1 = read_original_file(f"data\\original\\매매\\{i}_연립다세대(매매).csv")
        groupby_divison = df1["시군구"].unique().tolist()
        groupby_divison_list.update(groupby_divison)

    division_df = split_division(groupby_divison_list)
    division_df.to_csv(temp_division_file)
