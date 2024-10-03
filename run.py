from extract import extract_original_data
from main import begin_year, end_year, selected_division
from transform import transfer_groupby_yyyyMM

extract_original_data(begin_year, end_year, selected_division)
transfer_groupby_yyyyMM(begin_year, end_year, selected_division)
