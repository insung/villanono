import datetime

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from load_insight import get_dataframe_for_insight
from sidebar import add_sidebar
from util import get_data_file_path

#### variables ####
begin_year = 2020
end_year = 2024
si = "서울특별시"
gu = "서대문구"
dong = "북가좌동"

file_path = get_data_file_path(begin_year, end_year, si, gu, dong)

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
    "2020년 1월 1일 부터 2024년 10월 1일까지의 실거래 매매 정보입니다. 계속해서 업데이트할 예정입니다.",
    icon="🔥",
)
st.divider()

col1, col2, col3, col4 = st.columns(4)

size_choices = ["전체", "소형(60㎡미만)", "중형(80㎡미만)", "대형(80㎡이상)"]

today = datetime.datetime.today()
three_months_ago = today - datetime.timedelta(days=90)

with col1:
    st.selectbox(label="시", options=["서울특별시"])

with col2:
    st.selectbox(label="구", options=["서대문구"])

with col3:
    st.selectbox(label="동", options=["북가좌동"])

with col4:
    selected_size = st.selectbox(
        label="면적", options=size_choices, index=size_choices.index("전체")
    )

df = get_dataframe_for_insight(begin_year, end_year, si, gu, dong, selected_size)

df["계약년월"] = pd.to_datetime(df["계약년월"], format="%Y%m")

fig = make_subplots(
    rows=2,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.1,
    row_heights=[0.8, 0.2],
    subplot_titles=("평균(만원)", "거래량(건)"),
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
    # hovermode="x unified",
)
st.plotly_chart(fig, use_container_width=True)
