import streamlit as st

from page_config import set_page
from servies.insight_service import (
    load_buysell_data,
    load_buysell_rent_rate_data,
    load_rent_data,
)
from topbar import add_topbar

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

#### topbar ####
add_topbar(st)

tab1, tab2, tab3 = st.tabs(["매매 시장", "전세 시장", "전세가율"])

with tab1:
    st.header("매매 시장")
    st.dataframe(st.session_state["df_buysell"], use_container_width=True)

with tab2:
    st.header("전세 시장")
    st.dataframe(st.session_state["df_rent"], use_container_width=True)

with tab3:
    st.header("전세가율")
    st.dataframe(st.session_state["df_buysell_rent_rate"], use_container_width=True)

st.divider()

st.page_link(
    "📈인사이트.py", label="인사이트 페이지로 가기", icon="📈", use_container_width=True
)
