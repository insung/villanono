from os import path

__output_division_path = path.join("data", "output_divisions")

# def extract_division_data(
#     data_file_path: str, output_file_path: str, column: str = "시군구"
# ) -> str:
#     groupby_divison_set = set()
#     original_data_df = read_original_file(data_file_path)
#     groupby_divison = original_data_df[column].unique().tolist()
#     groupby_divison_set.update(groupby_divison)
#     output_file_path = merge_division_data(groupby_divison, output_file_path)
#     return output_file_path
