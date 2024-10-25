import datetime
import os

import streamlit as st

from page_config import add_page_config
from servies.insight_chart import load_chart
from sidebar import add_sidebar
from util import (
    get_dong_options,
    get_gu_options,
    get_si_options,
)

#### page config ####
add_page_config(st)

#### sidebar ####
add_sidebar(st)

#### session variables ####
today = datetime.datetime.today()
end_year: int = int(today.year)

if "begin_date" not in st.session_state:
    st.session_state["begin_date"] = today - datetime.timedelta(days=365)
    st.session_state["year_from_now"] = 1

if "selected_size" not in st.session_state:
    st.session_state["selected_size"] = "all"
    st.session_state["size_choice"] = "전체"

if "selected_si" not in st.session_state:
    st.session_state["si_list"] = get_si_options()

if "selected_gu" not in st.session_state:
    st.session_state["gu_list"] = get_gu_options()

if "selected_dong" not in st.session_state:
    st.session_state["dong_list"] = get_dong_options()

if "selectbox_dong_index" not in st.session_state:
    st.session_state["selectbox_dong_index"] = st.session_state["dong_list"].index(
        "북가좌동"
    )

if "selected_built_year" not in st.session_state:
    st.session_state["selected_built_year"] = "전체"

#### page ####

r1_col1, r1_col2, r1_col3 = st.columns(3)
r2_col1, r2_col2, r2_col3 = st.columns(3)

st.divider()

#### choices ####

choices_size = [
    "전체",
    "10평대 (33㎡미만)",
    "20평대 (66㎡미만)",
    "30평대 (99㎡미만)",
    "40평대 이상 (99㎡이상)",
]

indexes_size = [
    "",
    "10평대",
    "20평대",
    "30평대",
    "40평대 이상",
]

choices_begin_date = ["1년", "3년", "5년", "10년", "전체"]
indexes_begin_date = [
    today - datetime.timedelta(days=365),  # 1년
    today - datetime.timedelta(days=1095),  # 3년
    today - datetime.timedelta(days=1825),  # 5년
    today - datetime.timedelta(days=3650),  # 10년
    datetime.datetime(2006, 1, 1),
]

choices_built_year = ["전체", "~ 2년", "~ 4년", "~ 10년", "~ 20년", "~ 30년"]
indexes_built_year = [
    None,
    today - datetime.timedelta(days=730),  # 2년
    today - datetime.timedelta(days=1460),  # 4년
    today - datetime.timedelta(days=3650),  # 10년
    today - datetime.timedelta(days=7300),  # 20년
    today - datetime.timedelta(days=10950),  # 30년
]

#### colums work ####

with r1_col1:
    st.session_state["selected_si"] = st.selectbox(
        label="시",
        options=st.session_state["si_list"],
        index=st.session_state["si_list"].index("서울특별시"),
    )

with r1_col2:
    st.session_state["selected_gu"] = st.selectbox(
        label="구",
        options=st.session_state["gu_list"],
        index=st.session_state["gu_list"].index("서대문구"),
    )
    st.session_state["dong_list"] = get_dong_options(st.session_state["selected_gu"])

with r1_col3:
    try:
        st.session_state["selected_dong"] = st.selectbox(
            label="동",
            options=st.session_state["dong_list"],
            index=st.session_state["selectbox_dong_index"],
        )
    except:
        st.session_state["selectbox_dong_index"] = 0
        st.session_state["selected_dong"] = st.selectbox(
            label="동",
            options=st.session_state["dong_list"],
            index=st.session_state["selectbox_dong_index"],
        )

with r2_col1:
    selected_begin_date = st.selectbox(label="기간", options=choices_begin_date)

    if selected_begin_date == "전체":
        datetime_2006 = datetime.datetime(2006, 1, 1)
        st.session_state["begin_date"] = datetime_2006
        st.session_state["year_from_now"] = (
            f"{(today.year - datetime_2006.year) + 1} 년"
        )
    else:
        st.session_state["begin_date"] = indexes_begin_date[
            choices_begin_date.index(selected_begin_date)
        ]
        st.session_state["year_from_now"] = selected_begin_date

with r2_col2:
    size_choice = st.selectbox(
        label="면적", options=choices_size, index=choices_size.index("전체")
    )
    st.session_state["size_choice"] = size_choice
    st.session_state["selected_size"] = indexes_size[choices_size.index(size_choice)]

with r2_col3:
    selected_built_year = st.selectbox(
        label="건축년도",
        options=choices_built_year,
        index=choices_built_year.index("전체"),
        help="건축년도는 현재 날짜로부터의 경과 시간을 기준으로 계산됩니다. 예를 들어, 건축년도가 10년인 경우, 이는 현재 날짜로부터 10년 전에 지어진 건물까지 포함하여 조회됩니다.",
    )
    st.session_state["selected_built_year"] = indexes_built_year[
        choices_built_year.index(selected_built_year)
    ]

#### buysell ####

with st.expander("매매 시장", expanded=True):
    st.success("2006년 1월 1일 부터 2024년 10월 1일까지의 실거래 정보입니다.")
    file_path_buysell = os.path.join(
        "data",
        "temp3",
        "서울특별시",
        f"{st.session_state["selected_gu"]}_연립다세대(매매).csv",
    )
    load_chart(
        st,
        file_path_buysell,
        st.session_state["size_choice"],
        st.session_state["year_from_now"],
        st.session_state["begin_date"],
        st.session_state["selected_si"],
        st.session_state["selected_gu"],
        st.session_state["selected_dong"],
        st.session_state["selected_built_year"],
        st.session_state["selected_size"],
    )

with st.expander("전세 시장", expanded=False):
    st.success("2011년 1월 1일 부터 2024년 10월 1일까지의 실거래 정보입니다.")
    file_path_rent = os.path.join(
        "data",
        "temp3",
        "서울특별시",
        f"{st.session_state["selected_gu"]}_연립다세대(전월세).csv",
    )
    load_chart(
        st,
        file_path_rent,
        st.session_state["size_choice"],
        st.session_state["year_from_now"],
        st.session_state["begin_date"],
        st.session_state["selected_si"],
        st.session_state["selected_gu"],
        st.session_state["selected_dong"],
        st.session_state["selected_built_year"],
        st.session_state["selected_size"],
    )
