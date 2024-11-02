import os

import streamlit as st

from page_config import set_page
from servies.insight_chart import load_buysell_and_rent_percent, load_chart
from topbar import add_topbar

#### page config ####
set_page(st, False)

#### sidebar ####
# set_sidebar(st)

st.header("인사이트")

#### topbar ####
add_topbar(st)

#### charts ####

with st.expander("매매 시장", expanded=True):
    file_path_buysell = os.path.join(
        "data",
        "temp3",
        "서울특별시",
        f"{st.session_state["selected_gu"]}_연립다세대(매매).csv",
    )
    df_buysell = load_chart(
        st,
        file_path_buysell,
        st.session_state["size_choice"],
        st.session_state["year_from_now"],
        st.session_state["begin_date"],
        st.session_state["selected_si"],
        st.session_state["selected_gu"],
        st.session_state["selected_dong"],
        st.session_state["selected_built_year"],
        st.session_state["selected_size"],
    )
    st.session_state["df_buysell"] = df_buysell
    st.page_link(
        "pages/1_🌱매매 시장.py",
        label="매매 시장 데이터 자세히 보기",
        icon="🌱",
        use_container_width=True,
    )

with st.expander("전세 시장", expanded=True):
    file_path_rent = os.path.join(
        "data",
        "temp3",
        "서울특별시",
        f"{st.session_state["selected_gu"]}_연립다세대(전월세).csv",
    )
    df_rent = load_chart(
        st,
        file_path_rent,
        st.session_state["size_choice"],
        st.session_state["year_from_now"],
        st.session_state["begin_date"],
        st.session_state["selected_si"],
        st.session_state["selected_gu"],
        st.session_state["selected_dong"],
        st.session_state["selected_built_year"],
        st.session_state["selected_size"],
    )
    st.session_state["df_rent"] = df_rent
    st.page_link(
        "pages/2_💸전세 시장.py",
        label="전세 시장 데이터 자세히 보기",
        icon="💸",
        use_container_width=True,
    )

with st.expander("전세가율", expanded=True):
    df_merged = load_buysell_and_rent_percent(st, df_buysell, df_rent)
