from math import ceil

import numpy
import streamlit as st
from pandas import DataFrame

from components.page_config import set_page
from components.topbar import add_topbar
from servies.insight_service import (
    set_columns_round,
    set_columns_round_rate,
)


def _safe_stat(series, stat_func, default=0):
    """NaN 값을 무시하고 안전하게 통계치를 계산한 후 올림 처리합니다."""
    if series.dropna().empty:
        return default
    val = stat_func(series)
    return default if numpy.isnan(val) else ceil(val)


def _calculate_and_get_metrics(df: DataFrame) -> dict:
    """데이터프레임에서 주요 통계 지표를 계산하여 딕셔너리로 반환합니다."""
    if df.empty:
        return {"count": 0, "amount": 0, "min_amount": 0, "max_amount": 0}

    def safe_mean(series, round_to=0):
        """NaN 값을 무시하고 안전하게 평균을 계산한 후 올림 처리합니다."""
        val = series.mean()
        return 0 if numpy.isnan(val) else ceil(val.round(round_to))

    return {
        "count": safe_mean(df["거래량(건)"]),
        "amount": safe_mean(df["평균(만원)"], -2),
        "min_amount": safe_mean(df["최소(만원)"], -2),
        "max_amount": safe_mean(df["최대(만원)"], -2),
    }


def add_metrics(
    df_buysell: DataFrame, df_rent: DataFrame, df_buysell_rent_rate: DataFrame
):
    col1, col2, col3 = st.columns(3)
    year_from_now = st.session_state["year_from_now"]

    # 데이터가 없는 경우 오류를 방지하고 사용자에게 알림
    if df_buysell.empty or df_rent.empty:
        col1.metric(label=f"{year_from_now} 평균 월별 매매 거래량", value="N/A")
        col2.metric(label=f"{year_from_now} 평균 매매 금액", value="N/A")
        col3.metric(label=f"{year_from_now} 평균 전세가율", value="N/A")
        st.info(
            "선택하신 조건에 맞는 매매 또는 전세 데이터가 부족하여 상세 비교 정보를 표시할 수 없습니다."
        )
        return

    year_from_now = st.session_state["year_from_now"]

    buysell_metrics = _calculate_and_get_metrics(df_buysell)
    rent_metrics = _calculate_and_get_metrics(df_rent)

    rate_mean = df_buysell_rent_rate["전세가율(%)"].mean()
    avg_buysell_rate = 0 if numpy.isnan(rate_mean) else ceil(round(rate_mean))

    delta_avg_count = buysell_metrics["count"] - rent_metrics["count"]
    delta_avg_amount = buysell_metrics["amount"] - rent_metrics["amount"]
    delta_min_amount = buysell_metrics["min_amount"] - rent_metrics["min_amount"]
    delta_max_amount = buysell_metrics["max_amount"] - rent_metrics["max_amount"]

    col1.metric(
        label=f"{year_from_now} 평균 월별 매매 거래량",
        value=f"{buysell_metrics['count']} 건",
        delta=f"{delta_avg_count} 건 (전세대비)",
    )
    col2.metric(
        label=f"{year_from_now} 평균 매매 금액",
        value=f"{buysell_metrics['amount']:,.0f} 만원",
        delta=f"{delta_avg_amount:,.0f} 만원 (전세대비)",
    )
    col3.metric(label=f"{year_from_now} 평균 전세가율", value=f"{avg_buysell_rate}%")
    col1.metric(
        label=f"{year_from_now} 최소 매매 금액",
        value=f"{buysell_metrics['min_amount']:,.0f} 만원",
        delta=f"{(delta_min_amount):,.0f} 만원 (전세대비)",
    )
    col2.metric(
        label=f"{year_from_now} 최대 매매 금액",
        value=f"{buysell_metrics['max_amount']:,.0f} 만원",
        delta=f"{(delta_max_amount):,.0f} 만원 (전세대비)",
    )


def add_statistics(df: DataFrame):
    # 데이터가 없는 경우 오류를 방지하고 사용자에게 알림
    if df.empty:
        st.info("선택하신 조건에 맞는 데이터가 없습니다.")
        return

    amount_min = _safe_stat(df["평균(만원)"], numpy.min)
    amount_max = _safe_stat(df["평균(만원)"], numpy.max)
    amount_avg = _safe_stat(df["평균(만원)"], numpy.mean)

    count_min = _safe_stat(df["거래량(건)"], numpy.min)
    count_max = _safe_stat(df["거래량(건)"], numpy.max)
    buysell_dong_count = _safe_stat(df["거래량(건)"], numpy.mean)

    col1, col2 = st.columns(2)

    year_from_now = st.session_state["year_from_now"]
    selected_dong = st.session_state["selected_dong"]

    # st.slider의 파라미터를 동적으로 구성하여 코드 중복을 줄입니다.
    with col1:
        st.slider(
            "평균 가격(만원)",
            min_value=amount_min,
            max_value=amount_max,
            value=amount_avg,
            help=f"지난 {year_from_now} 간 {selected_dong} 의 평균 가격",
            disabled=(amount_min == amount_max),
        )

    with col2:
        st.slider(
            "거래량(건)",
            min_value=count_min,
            max_value=count_max,
            value=buysell_dong_count,
            help=f"지난 {year_from_now} 간 {selected_dong} 의 거래량",
            disabled=(count_min == count_max),
        )


def add_statistics_rate(df: DataFrame):
    # 데이터가 없는 경우 오류를 방지하고 사용자에게 알림
    if df.empty:
        st.info("선택하신 조건에 맞는 데이터가 없어 전세가율을 계산할 수 없습니다.")
        return

    rate_min = _safe_stat(df["전세가율(%)"], numpy.min)
    rate_max = _safe_stat(df["전세가율(%)"], numpy.max)
    rate_avg = _safe_stat(df["전세가율(%)"], numpy.mean)

    col1, col2 = st.columns(2)

    # 최소값과 최대값이 같을 경우 슬라이더를 비활성화하여 사용자 경험을 개선합니다.
    col1.slider(
        "전세가율(%)",
        min_value=rate_min,
        max_value=rate_max,
        value=rate_avg,
        disabled=(rate_min == rate_max),
    )


set_page(st, True)

st.header("통계 데이터")

#### topbar ####
add_topbar(st)

#### load data ####
df_buysell = st.session_state["df_buysell"].copy()
df_rent = st.session_state["df_rent"].copy()
df_buysell_rent_rate = st.session_state["df_buysell_rent_rate"].copy()
add_metrics(df_buysell, df_rent, df_buysell_rent_rate)

st.divider()

set_columns_round(df_buysell)
set_columns_round(df_rent)
set_columns_round_rate(df_buysell_rent_rate)

tab1, tab2, tab3 = st.tabs(["매매 시장", "전세 시장", "전세가율"])

with tab1:
    add_statistics(df_buysell)
    st.dataframe(df_buysell, use_container_width=True)

with tab2:
    add_statistics(df_rent)
    st.dataframe(df_rent, use_container_width=True)

with tab3:
    add_statistics_rate(df_buysell_rent_rate)
    st.dataframe(df_buysell_rent_rate, use_container_width=True)

st.divider()

st.page_link(
    "pages/1_📈인사이트.py",
    label="인사이트 페이지로 가기",
    icon="📈",
    use_container_width=True,
)
