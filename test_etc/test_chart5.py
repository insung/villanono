# 예시 데이터프레임
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

df = pd.DataFrame(
    {
        "계약년월": ["2023-01", "2023-02", "2023-03"],
        "평균(만원)": [1000, 1500, 2000],
        "거래량(건)": [10, 20, 30],
    }
)

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

fig.update_xaxes(tickformat="%Y-%m")
fig.update_yaxes(tickformat=",.0f")
fig.update_layout(height=600, showlegend=False)
st.plotly_chart(fig, use_container_width=True)
