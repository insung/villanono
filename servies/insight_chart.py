from datetime import datetime

import pandas as pd
import plotly.graph_objects as go
import streamlit
from plotly.subplots import make_subplots

from servies.insight_query import get_insight_query


def load_chart(
    st: streamlit,
    file_path: str,
    size_choice: str,
    year_from_now: str,
    begin_date: datetime,
    selected_si: str,
    selected_gu: str,
    selected_dong: str,
    selected_built_year: datetime | None,
    selected_size: str | None,
) -> pd.DataFrame:
    query = get_insight_query(
        begin_date,
        selected_si,
        selected_gu,
        selected_dong,
        selected_built_year,
        selected_size,
    )

    begin_yyyyMM = int(begin_date.strftime("%Y%m"))

    read_df = pd.read_csv(file_path)
    df = (
        read_df.query(query)
        .groupby(["계약년월"], as_index=False)
        .agg(
            {
                "거래금액(만원)": [
                    "count",
                    "mean",
                    "std",
                    "min",
                    lambda x: x.quantile(0.25),
                    "median",
                    lambda x: x.quantile(0.75),
                    "max",
                ]
            }
        )
    )

    df.columns = [
        "계약년월",
        "거래량(건)",
        "평균(만원)",
        "표준편차(만원)",
        "최소(만원)",
        "25%",
        "50%",
        "75%",
        "최대(만원)",
    ]
    df["평균(만원)"] = df["평균(만원)"].round(2)

    #### charts ####

    if df is None:
        st.write("데이터가 없습니다.")
        return

    df = df.query(f"계약년월 > {begin_yyyyMM}")

    df["계약년월"] = pd.to_datetime(df["계약년월"], format="%Y%m")

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

    return df


def load_buysell_and_rent_percent(
    st: streamlit, df_buysell: pd.DataFrame, df_rent: pd.DataFrame
):
    # 데이터프레임 병합
    df_merged = pd.merge(
        df_buysell, df_rent, on="계약년월", suffixes=("_매매", "_전세")
    )

    # 전세가율 계산
    df_merged["전세가율(%)"] = (
        df_merged["평균(만원)_전세"] / df_merged["평균(만원)_매매"]
    ) * 100

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


def load_buysell_and_rent_percent2(
    st: streamlit, df_buysell: pd.DataFrame, df_rent: pd.DataFrame
):
    # 데이터프레임 병합
    df_merged = pd.merge(
        df_buysell, df_rent, on="계약년월", suffixes=("_매매", "_전세")
    )

    # 전세가율 계산
    df_merged["전세가율(%)"] = (
        df_merged["평균(만원)_전세"] / df_merged["평균(만원)_매매"]
    ) * 100

    # Plotly를 사용한 라인차트 생성
    fig = go.Figure()

    # 매매가 평균 라인
    fig.add_trace(
        go.Scatter(
            x=df_merged["계약년월"],
            y=df_merged["평균(만원)_매매"],
            mode="lines+markers",
            name="매매가 평균(만원)",
        )
    )

    # 전세가 평균 라인
    fig.add_trace(
        go.Scatter(
            x=df_merged["계약년월"],
            y=df_merged["평균(만원)_전세"],
            mode="lines+markers",
            name="전세가 평균(만원)",
        )
    )

    # 전세가율 라인 (보조 축 사용)
    fig.add_trace(
        go.Scatter(
            x=df_merged["계약년월"],
            y=df_merged["전세가율(%)"],
            mode="lines+markers",
            name="전세가율(%)",
            yaxis="y2",
        )
    )

    # 레이아웃 설정
    fig.update_layout(
        title="매매가 평균, 전세가 평균, 전세가율 라인차트",
        xaxis_title="계약년월",
        yaxis_title="가격(만원)",
        yaxis2=dict(title="전세가율(%)", overlaying="y", side="right"),
    )

    # Streamlit을 사용하여 차트 표시
    st.plotly_chart(fig)


def load_buysell_and_rent_percent3(
    st: streamlit, df_buysell: pd.DataFrame, df_rent: pd.DataFrame
):
    # 데이터프레임 병합
    df_merged = pd.merge(
        df_buysell, df_rent, on="계약년월", suffixes=("_매매", "_전세")
    )

    # 전세가율 계산
    df_merged["전세가율(%)"] = (
        df_merged["평균(만원)_전세"] / df_merged["평균(만원)_매매"]
    ) * 100

    # Subplots 생성
    fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=("매매가 평균(만원)", "전세가 평균(만원)", "전세가율(%)"),
    )

    # 매매가 평균 라인
    fig.add_trace(
        go.Scatter(
            x=df_merged["계약년월"],
            y=df_merged["평균(만원)_매매"],
            mode="lines+markers",
            name="매매가 평균(만원)",
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
            name="전세가 평균(만원)",
        ),
        row=2,
        col=1,
    )

    # 전세가율 라인
    fig.add_trace(
        go.Scatter(
            x=df_merged["계약년월"],
            y=df_merged["전세가율(%)"],
            mode="lines+markers",
            name="전세가율(%)",
        ),
        row=3,
        col=1,
    )

    # 레이아웃 설정
    fig.update_layout(
        height=800, title_text="매매가 평균, 전세가 평균, 전세가율 Subplots"
    )

    # Streamlit을 사용하여 차트 표시
    st.plotly_chart(fig)
