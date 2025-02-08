import pandas as pd
import plotly.graph_objects as go
import streamlit
from plotly.subplots import make_subplots


def load_chart(
    st: streamlit,
    df: pd.DataFrame,
    size_choice: str,
    year_from_now: str,
):
    if df is None:
        st.write("데이터가 없습니다.")
        return

    #### charts ####
    sub_chart_mean = df["평균(만원)"].mean()
    sub_chart_mean_title = f"{size_choice} 면적 - 지난 {year_from_now} 간 평균 ({sub_chart_mean:,.0f} 만원)"

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


def load_chart_buysell_rent_rate(st: streamlit, df_merged: pd.DataFrame):
    if df_merged is None:
        st.write("데이터가 없습니다.")
        return

    # Subplots 생성
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        row_heights=[0.8, 0.2],
        subplot_titles=("매매/전세", "전세가율(%)"),
    )

    # 매매가 평균 라인
    fig.add_trace(
        go.Scatter(
            x=df_merged["계약년월"],
            y=df_merged["평균(만원)_매매"],
            hovertemplate="%{x|%Y-%m} - %{y}만원",
            name="",
        ),
        row=1,
        col=1,
    )

    # 전세가 평균 라인
    fig.add_trace(
        go.Scatter(
            x=df_merged["계약년월"],
            y=df_merged["평균(만원)_전세"],
            mode="lines+markers",
            hovertemplate="%{x|%Y-%m} - %{y}만원",
            name="",
        ),
        row=1,
        col=1,
    )

    # 전세가율 라인
    fig.add_trace(
        go.Bar(
            x=df_merged["계약년월"],
            y=df_merged["전세가율(%)"],
            name="전세가율(%)",
        ),
        row=2,
        col=1,
    )

    fig.update_yaxes(tickformat=",.0f")

    # 레이아웃 설정
    fig.update_layout(
        height=600,
        showlegend=False,
        xaxis=dict(
            rangeslider=dict(visible=False),
        ),
        hovermode="x unified",
    )

    # Streamlit을 사용하여 차트 표시
    st.plotly_chart(fig, use_container_width=True)
