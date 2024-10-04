import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from load_insight import get_dataframe_for_insight
from sidebar import get_sidebar
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
    page_title="빌라 실거래가 검색은 빌라 노노 | 베타버전",
    page_icon="🚀",
    # layout="wide",
    # initial_sidebar_state="expanded",
)

#### sidebar ####
get_sidebar(st)

#### index page ####
st.header("안녕하세요! 빌라 노노입니다. ✨")

st.success(
    "서울시 서대문구 북가좌동 2020년 1월 1일 부터 2024년 10월 1일까지의 실거래 매매 정보입니다. 계속해서 업데이트할 예정입니다.",
    icon="🔥",
)
st.divider()


col1, col2, col3 = st.columns(3)

default_value = "거래량(건)"

choices = [
    "거래량(건)",
    "종합",
    "평균(만원)",
    "표준편차(만원)",
    "최소(만원)",
    "25%",
    "50%",
    "75%",
    "최대(만원)",
]

size_choices = ["전체", "소형(60㎡미만)", "중형(80㎡미만)", "대형(80㎡이상)"]

with col1:
    selected_size = st.selectbox(
        label="면적:", options=size_choices, index=size_choices.index("전체")
    )

with col3:
    selected = st.selectbox(
        label="지표:", options=choices, index=choices.index(default_value)
    )

df = get_dataframe_for_insight(begin_year, end_year, si, gu, dong, selected_size)

df["계약년월"] = pd.to_datetime(df["계약년월"], format="%Y%m")
tickvals = df["계약년월"]
ticktext = df["계약년월"].dt.strftime("%Y-%m")

if selected == "종합":
    fig = px.line(df, x="계약년월", y="평균(만원)", markers=True)
    fig.update_xaxes(type="category", tickvals=tickvals, ticktext=ticktext)
    fig.update_yaxes(tickformat=",.0f")
    fig.add_scatter(
        x=df["계약년월"],
        y=df["최소(만원)"],
        mode="markers",
        name="최소",
        marker=dict(color="#E8E8E8", size=5),
        hoverinfo="none",
        showlegend=False,
    )
    fig.add_scatter(
        x=df["계약년월"],
        y=df["최대(만원)"],
        mode="markers",
        name="최대",
        marker=dict(color="#E8E8E8", size=5),
        hoverinfo="none",
        showlegend=False,
    )

    fig.update_traces(
        hovertemplate="<b>%{x}</b><br /><br />평균(만원): %{customdata[0]:,.0f}<br />최소(만원): %{customdata[1]:,.0f}<br />최대(만원): %{customdata[2]:,.0f}",
        customdata=df[["평균(만원)", "최소(만원)", "최대(만원)"]].values,
    )
    st.plotly_chart(fig)
elif selected == "거래량(건)":
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        row_heights=[0.8, 0.2],
        subplot_titles=("가격(만원)", "거래량(건)"),
    )

    fig.add_trace(go.Scatter(x=df["계약년월"], y=df["평균(만원)"]), row=1, col=1)

    fig.add_trace(go.Bar(x=df["계약년월"], y=df["거래량(건)"]), row=2, col=1)
    fig.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
else:
    fig = px.line(df, x="계약년월", y=selected)
    fig.update_xaxes(type="category", tickvals=tickvals, ticktext=ticktext)
    fig.update_yaxes(tickformat=",.0f")

    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(step="all"),
                    ]
                )
            ),
            rangeslider=dict(visible=True),
            type="date",
        )
    )

    st.plotly_chart(fig)


# df["계약년월"] = df["계약년월"].dt.strftime("%Y-%m")
# st.dataframe(df, hide_index=True)

# st.write(df["계약년월"].min(), df["계약년월"].max())
# print(type(df["계약년월"].min()))
