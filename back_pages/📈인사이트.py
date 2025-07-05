import streamlit as st
from topbar import add_topbar

from components.page_config import set_page
from servies.insight_chart import load_chart, load_chart_buysell_rent_rate

#### page config ####
set_page(st, False)

#### sidebar ####
# set_sidebar(st)

st.header("인사이트")

#### topbar ####
add_topbar(st)

#### charts ####
with st.expander("매매 시장", expanded=True):
    load_chart(
        st,
        st.session_state["df_buysell"],
        st.session_state["size_choice"],
        st.session_state["year_from_now"],
    )
    st.page_link(
        "pages/1_🧐통계 데이터.py",
        label="데이터 자세히 보기",
        icon="🧐",
        use_container_width=True,
    )

with st.expander("전세 시장", expanded=True):
    load_chart(
        st,
        st.session_state["df_rent"],
        st.session_state["size_choice"],
        st.session_state["year_from_now"],
    )
    st.page_link(
        "pages/1_🧐통계 데이터.py",
        label="데이터 자세히 보기",
        icon="🧐",
        use_container_width=True,
    )

with st.expander("전세가율", expanded=True):
    load_chart_buysell_rent_rate(st, st.session_state["df_buysell_rent_rate"])
    st.page_link(
        "pages/1_🧐통계 데이터.py",
        label="데이터 자세히 보기",
        icon="🧐",
        use_container_width=True,
    )
