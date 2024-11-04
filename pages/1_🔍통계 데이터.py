from math import ceil

import streamlit as st
from pandas import DataFrame

from page_config import set_page
from servies.insight_service import (
    load_buysell_data,
    load_buysell_rent_rate_data,
    load_rent_data,
    set_columns_round,
    set_columns_round_rate,
)
from topbar import add_topbar


def add_metric(
    df_buysell: DataFrame, df_rent: DataFrame, df_buysell_rent_rate: DataFrame
):
    col1, col2, col3 = st.columns(3)
    year_from_now = st.session_state["year_from_now"]

    avg_buysell_count = ceil(df_buysell["거래량(건)"].mean().round(0))
    avg_buysell_amount = ceil(df_buysell["평균(만원)"].mean().round(-2))
    min_buysell_amount = ceil(df_buysell["최소(만원)"].mean().round(-2))
    max_buysell_amount = ceil(df_buysell["최대(만원)"].mean().round(-2))
    avg_buysell_rate = ceil(df_buysell_rent_rate["전세가율(%)"].mean().round(0))

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


set_page(st, True)

if "df_buysell" not in st.session_state:
    st.session_state["df_buysell"] = load_buysell_data(
        st.session_state["begin_date"],
        st.session_state["selected_si"],
        st.session_state["selected_gu"],
        st.session_state["selected_dong"],
        st.session_state["selected_built_year"],
        st.session_state["selected_size"],
    )

if "df_rent" not in st.session_state:
    st.session_state["df_rent"] = load_rent_data(
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

df_buysell = st.session_state["df_buysell"].copy()
df_rent = st.session_state["df_rent"].copy()
df_buysell_rent_rate = st.session_state["df_buysell_rent_rate"].copy()
add_metric(df_buysell, df_rent, df_buysell_rent_rate)

st.divider()

tab1, tab2, tab3 = st.tabs(["매매 시장", "전세 시장", "전세가율"])

with tab1:
    set_columns_round(df_buysell)
    st.dataframe(df_buysell, use_container_width=True)

with tab2:
    set_columns_round(df_rent)
    st.dataframe(df_rent, use_container_width=True)

with tab3:
    set_columns_round_rate(df_buysell_rent_rate)
    st.dataframe(df_buysell_rent_rate, use_container_width=True)


st.divider()

st.page_link(
    "📈인사이트.py", label="인사이트 페이지로 가기", icon="📈", use_container_width=True
)
