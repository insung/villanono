import datetime
from typing import Any

import streamlit

from util import get_dong_options, get_gu_options, get_si_options


def init_session_variables(st: streamlit):
    today = datetime.datetime.today()
    __init_if_empty(st, "begin_date", today - datetime.timedelta(days=365))
    __init_if_empty(st, "year_from_now", 1)
    __init_if_empty(st, "selected_begin_date", "1년")

    __init_if_empty(st, "si_list", get_si_options())
    __init_if_empty(st, "gu_list", get_gu_options())
    __init_if_empty(st, "dong_list", get_dong_options())

    __init_if_empty(st, "selected_size", "")
    __init_if_empty(st, "size_choice", "전체")

    __init_if_empty(st, "selected_si", "서울특별시")
    __init_if_empty(st, "selected_gu", "서대문구")
    __init_if_empty(st, "selected_dong", "북가좌동")

    __init_if_empty(st, "selected_built_year", None)
    __init_if_empty(st, "built_year_choice", "전체")

    __init_if_empty(st, "selected_datatype", ["매매", "전세", "월세"])

    __init_if_empty(st, "last_moved_center", None)
    __init_if_empty(st, "last_moved_si_gu_dong", None)
    __init_if_empty(st, "locations", [])
    __init_if_empty(st, "folium_data", None)


def __init_if_empty(st: streamlit, key: str, value: Any):
    if key not in st.session_state:
        st.session_state[key] = value
