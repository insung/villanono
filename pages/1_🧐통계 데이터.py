from math import ceil

import numpy
import streamlit as st
from pandas import DataFrame

from page_config import set_page
from servies.insight_service import (
    load_buysell_data_with_api,
    load_buysell_rent_rate_data,
    set_columns_round,
    set_columns_round_rate,
)
from topbar import add_topbar


def add_metrics(
    df_buysell: DataFrame, df_rent: DataFrame, df_buysell_rent_rate: DataFrame
):
    col1, col2, col3 = st.columns(3)
    year_from_now = st.session_state["year_from_now"]

    avg_buysell_count = ceil(df_buysell["거래량(건)"].mean().round(0))
    avg_buysell_amount = ceil(df_buysell["평균(만원)"].mean().round(-2))
    min_buysell_amount = ceil(df_buysell["최소(만원)"].mean().round(-2))
    max_buysell_amount = ceil(df_buysell["최대(만원)"].mean().round(-2))
    avg_buysell_rate_mean = (
        0
        if numpy.isnan(df_buysell_rent_rate["전세가율(%)"].mean())
        else df_buysell_rent_rate["전세가율(%)"].mean()
    )
    avg_buysell_rate = ceil(round(avg_buysell_rate_mean))

    avg_rent_count = ceil(df_rent["거래량(건)"].mean().round(0))
    avg_rent_amount = ceil(df_rent["평균(만원)"].mean().round(-2))
    min_rent_amount = ceil(df_rent["최소(만원)"].mean().round(-2))
    max_rent_amount = ceil(df_rent["최대(만원)"].mean().round(-2))

    delta_avg_count = avg_buysell_count - avg_rent_count
    delta_avg_amount = avg_buysell_amount - avg_rent_amount
    delta_min_amount = min_buysell_amount - min_rent_amount
    delta_max_amount = max_buysell_amount - max_rent_amount

    col1.metric(
        label=f"{year_from_now} 평균 월별 매매 거래량",
        value=f"{avg_buysell_count} 건",
        delta=f"{delta_avg_count} 건 (전세대비)",
    )
    col2.metric(
        label=f"{year_from_now} 평균 매매 금액",
        value=f"{avg_buysell_amount:,.0f} 만원",
        delta=f"{delta_avg_amount:,.0f} 만원 (전세대비)",
    )
    col3.metric(label=f"{year_from_now} 평균 전세가율", value=f"{avg_buysell_rate}%")
    col1.metric(
        label=f"{year_from_now} 최소 매매 금액",
        value=f"{min_buysell_amount:,.0f} 만원",
        delta=f"{(delta_min_amount):,.0f} 만원 (전세대비)",
    )
    col2.metric(
        label=f"{year_from_now} 최대 매매 금액",
        value=f"{max_buysell_amount:,.0f} 만원",
        delta=f"{(delta_max_amount):,.0f} 만원 (전세대비)",
    )


def add_statistics(df: DataFrame):
    amount_min = ceil(df["평균(만원)"].min())
    amount_max = ceil(df["평균(만원)"].max())
    amount_avg = ceil(df["평균(만원)"].mean().round(0))

    count_min = ceil(df["거래량(건)"].min())
    count_max = ceil(df["거래량(건)"].max())
    buysell_dong_count = ceil(df["거래량(건)"].mean().round(0))

    col1, col2 = st.columns(2)

    year_from_now = st.session_state["year_from_now"]
    selected_dong = st.session_state["selected_dong"]

    with col1:
        if amount_min == amount_max:
            st.slider(
                "평균 가격(만원)",
                value=amount_avg,
                max_value=amount_max,
                help=f"지난 {year_from_now} 간 {selected_dong} 의 평균 가격",
            )
        else:
            st.slider(
                "평균 가격(만원)",
                value=amount_avg,
                min_value=amount_min,
                max_value=amount_max,
                help=f"지난 {year_from_now} 간 {selected_dong} 의 평균 가격",
            )

    with col2:
        if count_min == count_max:
            st.slider(
                "거래량(건)",
                value=buysell_dong_count,
                max_value=count_max,
                help=f"지난 {year_from_now} 간 {selected_dong} 의 거래량",
            )
        else:
            st.slider(
                "거래량(건)",
                value=buysell_dong_count,
                min_value=count_min,
                max_value=count_max,
                help=f"지난 {year_from_now} 간 {selected_dong} 의 거래량",
            )


def add_statistics_rate(df: DataFrame):
    rate_min = ceil(
        0 if numpy.isnan(df["전세가율(%)"].min()) else df["전세가율(%)"].min()
    )
    rate_max = ceil(
        0 if numpy.isnan(df["전세가율(%)"].max()) else df["전세가율(%)"].max()
    )
    rate_avg_mean = (
        0 if numpy.isnan(df["전세가율(%)"].mean()) else df["전세가율(%)"].mean()
    )
    rate_avg = ceil(round(rate_avg_mean))

    col1, col2 = st.columns(2)

    if rate_min == rate_max:
        col1.slider(
            "전세가율(%)",
            value=rate_avg,
        )
    else:
        col1.slider(
            "전세가율(%)",
            value=rate_avg,
            min_value=rate_min,
            max_value=rate_max,
        )


set_page(st, True)

#### sessions ####
if "df_buysell" not in st.session_state:
    st.session_state["df_buysell"] = load_buysell_data_with_api(
        "BuySell",
        st.session_state["begin_date"],
        st.session_state["selected_si"],
        st.session_state["selected_gu"],
        st.session_state["selected_dong"],
        st.session_state["selected_built_year"],
        st.session_state["selected_size"],
    )

if "df_rent" not in st.session_state:
    st.session_state["df_rent"] = load_buysell_data_with_api(
        "Rent",
        st.session_state["begin_date"],
        st.session_state["selected_si"],
        st.session_state["selected_gu"],
        st.session_state["selected_dong"],
        st.session_state["selected_built_year"],
        st.session_state["selected_size"],
    )

if "df_buysell_rent_rate" not in st.session_state:
    st.session_state["df_buysell_rent_rate"] = load_buysell_rent_rate_data(
        st.session_state["df_buysell"], st.session_state["df_rent"]
    )

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
    st.markdown("<br />", unsafe_allow_html=True)
    add_statistics(df_buysell)
    st.markdown("<br />", unsafe_allow_html=True)
    st.dataframe(df_buysell, use_container_width=True)

with tab2:
    st.markdown("<br />", unsafe_allow_html=True)
    add_statistics(df_rent)
    st.markdown("<br />", unsafe_allow_html=True)
    st.dataframe(df_rent, use_container_width=True)

with tab3:
    st.markdown("<br />", unsafe_allow_html=True)
    add_statistics_rate(df_buysell_rent_rate)
    st.markdown("<br />", unsafe_allow_html=True)
    st.dataframe(df_buysell_rent_rate, use_container_width=True)

st.divider()

st.page_link(
    "📈인사이트.py", label="인사이트 페이지로 가기", icon="📈", use_container_width=True
)
