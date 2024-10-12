import datetime

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from sidebar import add_sidebar
from util import (
    get_dataframe_for_insight,
    get_dong_options,
    get_gu_options,
    get_si_options,
)

#### variables ####
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

#### config ####
st.set_page_config(
    page_title="빌라 실거래 검색은 빌라 노노 | 베타버전",
    page_icon="🚀",
    # layout="wide",
    # initial_sidebar_state="expanded",
)

#### sidebar ####
add_sidebar(st)

#### index page ####
st.success(
    "2006년 1월 1일 부터 2024년 10월 1일까지의 실거래 매매 정보입니다. 계속해서 업데이트할 예정입니다.",
    icon="🔥",
)
st.divider()

col1, col2, col3, col4 = st.columns(4)

size_choices = [
    "전체",
    "10평대 (33㎡미만)",
    "20평대 (66㎡미만)",
    "30평대 (99㎡미만)",
    "40평대 이상 (99㎡이상)",
]

selected_sizes = [
    "all",
    "under_20",
    "under_30",
    "under_40",
    "over_40",
]


with col1:
    st.session_state["selected_si"] = st.selectbox(
        label="시",
        options=st.session_state["si_list"],
        index=st.session_state["si_list"].index("서울특별시"),
    )

with col2:
    st.session_state["selected_gu"] = st.selectbox(
        label="구",
        options=st.session_state["gu_list"],
        index=st.session_state["gu_list"].index("서대문구"),
    )

    st.session_state["dong_list"] = get_dong_options(st.session_state["selected_gu"])


with col3:
    st.session_state["selected_dong"] = st.selectbox(
        label="동",
        options=st.session_state["dong_list"],
        index=st.session_state["selectbox_dong_index"],
    )

with col4:
    size_choice = st.selectbox(
        label="면적", options=size_choices, index=size_choices.index("전체")
    )
    st.session_state["size_choice"] = size_choice
    st.session_state["selected_size"] = selected_sizes[size_choices.index(size_choice)]

b_col1, b_col2, b_col3, b_col4, b_col5, b_col6 = st.columns(6)

if b_col2.button("1년", use_container_width=True):
    st.session_state["begin_date"] = today - datetime.timedelta(days=365)
    st.session_state["year_from_now"] = 1
if b_col3.button("3년", use_container_width=True):
    st.session_state["begin_date"] = today - datetime.timedelta(days=1095)
    st.session_state["year_from_now"] = 3
if b_col4.button("5년", use_container_width=True):
    st.session_state["begin_date"] = today - datetime.timedelta(days=1825)
    st.session_state["year_from_now"] = 5
if b_col5.button("10년", use_container_width=True):
    st.session_state["begin_date"] = today - datetime.timedelta(days=3650)
    st.session_state["year_from_now"] = 10
if b_col6.button("전체", use_container_width=True):
    datetime_2006 = datetime.datetime(2006, 1, 1)
    st.session_state["begin_date"] = datetime_2006
    st.session_state["year_from_now"] = (today.year - datetime_2006.year) + 1


begin_yyyyMM = int(st.session_state["begin_date"].strftime("%Y%m"))
begin_year = int(st.session_state["begin_date"].year)

df = get_dataframe_for_insight(
    begin_year,
    end_year,
    st.session_state["selected_si"],
    st.session_state["selected_gu"],
    st.session_state["selected_dong"],
    st.session_state["selected_size"],
)

if df is None:
    st.write("데이터가 없습니다.")
else:
    df = df.query(f"계약년월 > {begin_yyyyMM}")

    df["계약년월"] = pd.to_datetime(df["계약년월"], format="%Y%m")

    sub_chart_mean = df["평균(만원)"].mean()
    sub_chart_mean_title = f"{st.session_state["size_choice"]} 지난 {st.session_state["year_from_now"]} 년간 평균 ({sub_chart_mean:,.0f} 만원)"

    sub_chart_count = df["거래량(건)"].sum()
    sub_chart_count_title = f"거래량 ({sub_chart_count:,.0f} 건)"

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        row_heights=[0.8, 0.2],
        subplot_titles=(sub_chart_mean_title, sub_chart_count_title),
    )

    fig.add_trace(
        go.Scatter(
            x=df["계약년월"],
            y=df["평균(만원)"],
            hovertemplate="%{x|%Y-%m} - %{y}만원",
            name="",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Bar(
            x=df["계약년월"],
            y=df["거래량(건)"],
            hovertemplate="%{x|%Y-%m} - %{y}건",
            name="",
        ),
        row=2,
        col=1,
    )
    fig.update_yaxes(tickformat=",.0f")
    fig.update_layout(
        height=600,
        showlegend=False,
        xaxis=dict(
            rangeslider=dict(visible=False),
        ),
        hovermode="x unified",
    )
    st.plotly_chart(fig, use_container_width=True)
