import streamlit as st

from page_config import set_page
from sidebar import set_sidebar

#### page config ####
set_page(st, False)

#### sidebar ####
set_sidebar(st)

st.header("릴리즈 노트")

st.write("2024-10-04 : 사이트 Open")
st.write(
    "2024-10-09 : 2006년도 부터 검색가능하도록 개선, 소형/중형/대형 이던 면적을 세분화"
)
st.write("2024-10-12 : 서울특별시 서대문구 북가좌동에서 서울 전체로 기능 확대")
st.write("2024-10-20 : 건축년도 별로 인사이트 조회 기능 추가")
st.write("2024-10-26 : 전세 시장 인사이트 조회 기능 추가")
st.write("2024-10-31 : 전세가율 기능 추가")
st.write("2024-11-03 : 자세히 보기(통계 데이터) 기능 추가")
st.write("2024-11-05 : 통계 데이터의 대표 수치 표시")
st.write("2024-11-16 : 2024년 10월 31일까지 조회되도록 데이터 갱신")

st.divider()

st.subheader("🔥앞으로의 계획")
st.write("통계 데이터 중 세부 검색 가능하도록 기능 추가 필요")
st.write("RAW 데이터 조회 기능")
st.write("주소로 빌라 실거래 검색 기능")
st.write("지도 기능")
