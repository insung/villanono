from main import begin_year, end_year, selected_division

from etl.extract import extract_original_data
from etl.transform import transfer_groupby_yyyyMM

extract_original_data(begin_year, end_year, selected_division)
transfer_groupby_yyyyMM(begin_year, end_year, selected_division)
