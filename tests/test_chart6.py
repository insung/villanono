# 예시 데이터프레임
import datetime

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

df = pd.DataFrame(
    {
        "계약년월": [
            "2021-01",
            "2021-02",
            "2021-03",
            "2021-04",
            "2021-05",
            "2021-06",
            "2021-07",
            "2021-08",
            "2021-09",
            "2021-10",
            "2021-11",
            "2021-12",
            "2022-01",
            "2022-02",
            "2022-03",
            "2022-04",
            "2022-05",
            "2022-06",
            "2022-07",
            "2022-08",
            "2022-09",
            "2022-10",
            "2022-11",
            "2022-12",
            "2023-01",
            "2023-02",
            "2023-03",
        ],
        "평균(만원)": [
            1000,
            1500,
            2000,
            1800,
            1700,
            1600,
            1500,
            1400,
            1300,
            1200,
            1100,
            1000,
            900,
            800,
            700,
            600,
            500,
            400,
            300,
            200,
            100,
            50,
            25,
            10,
            5,
            2,
            1,
        ],
        "거래량(건)": [
            10,
            20,
            30,
            25,
            20,
            15,
            10,
            5,
            3,
            2,
            1,
            0,
            5,
            10,
            15,
            20,
            25,
            30,
            35,
            40,
            45,
            50,
            55,
            60,
            65,
            70,
            75,
        ],
    }
)

# 현재 날짜와 3개월 전 날짜 계산
today = datetime.datetime.today()
three_months_ago = today - datetime.timedelta(days=90)

fig = make_subplots(
    rows=2,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.1,
    row_heights=[0.8, 0.2],
    subplot_titles=("가격(만원)", "거래량(건)"),
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
        rangeselector=dict(
            buttons=list(
                [
                    dict(count=1, label="1년", step="year", stepmode="backward"),
                    dict(count=3, label="3년", step="year", stepmode="backward"),
                    dict(count=10, label="10년", step="year", stepmode="backward"),
                    dict(step="all", label="전체", visible=False),
                ]
            ),
            activecolor="blue",  # 선택된 버튼 색상 설정
        ),
        rangeslider=dict(visible=False),
        type="date",
        range=[
            three_months_ago.strftime("%Y-%m-%d"),
            today.strftime("%Y-%m-%d"),
        ],  # 3년 범위 설정
    ),
)
st.plotly_chart(fig, use_container_width=True)
