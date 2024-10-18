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
    page_title="빌라 실거래 검색은 빌라 노노",
    page_icon="🚀",
    # layout="wide",
    # initial_sidebar_state="expanded",
)

#### sidebar ####
add_sidebar(st)

# 전세는 2011년 1월 1일 부터

#### index page ####
st.success("2006년 1월 1일 부터 2024년 10월 1일까지의 실거래 정보입니다.")
st.divider()

r1_col1, r1_col2, r1_col3 = st.columns(3)
r2_col1, r2_col2, r2_col3 = st.columns(3)

st.divider()

choices_size = [
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

choices_begin_date = ["1년", "3년", "5년", "10년", "전체"]
selected_begin_dates = [
    today - datetime.timedelta(days=365),  # 1년
    today - datetime.timedelta(days=1095),  # 3년
    today - datetime.timedelta(days=1825),  # 5년
    today - datetime.timedelta(days=3650),  # 10년
    datetime.datetime(2006, 1, 1),
]

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
        st.session_state["begin_date"] = selected_begin_dates[
            choices_begin_date.index(selected_begin_date)
        ]
        st.session_state["year_from_now"] = selected_begin_date

with r2_col2:
    size_choice = st.selectbox(
        label="면적", options=choices_size, index=choices_size.index("전체")
    )
    st.session_state["size_choice"] = size_choice
    st.session_state["selected_size"] = selected_sizes[choices_size.index(size_choice)]

with r2_col3:
    size_choice = st.selectbox(
        label="건축년도",
        options=["~ 2년", "~ 4년", "~ 10년", "~ 20년", "~ 30년"],
        disabled=True,
    )

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
    sub_chart_mean_title = f"{st.session_state["size_choice"]} 면적 - 지난 {st.session_state["year_from_now"]} 간 평균 ({sub_chart_mean:,.0f} 만원)"

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
