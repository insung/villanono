import streamlit as st

from page_config import add_page_config
from sidebar import add_sidebar

#### page config ####
add_page_config(st)

#### sidebar ####
add_sidebar(st)

st.write("2024-10-04 : 사이트 Open")
st.write(
    "2024-10-09 : 2006년도 부터 검색가능하도록 개선, 소형/중형/대형 이던 면적을 세분화"
)
st.write("2024-10-12 : 서울특별시 서대문구 북가좌동에서 서울 전체로 기능 확대")
st.write("2024-10-19 : 건축년도 별로 인사이트 조회 기능 추가")

st.divider()

st.write("🔥앞으로의 계획")
st.markdown("~~서울특별시 서대문구 북가좌동에서 서울 전체로 기능 확대~~")
st.write("주소로 빌라 실거래 검색 기능")
