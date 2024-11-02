import streamlit as st

from page_config import set_page
from topbar import add_topbar

set_page(st, True)

if "df_rent" not in st.session_state:
    st.switch_page("📈인사이트.py")

st.header("전세 시장")

st.success("2011년 1월 1일 부터 2024년 10월 1일까지의 실거래 정보입니다.")

#### topbar ####
add_topbar(st)

st.dataframe(st.session_state["df_rent"], use_container_width=True)

st.page_link(
    "📈인사이트.py", label="인사이트 페이지로 가기", icon="📈", use_container_width=True
)
