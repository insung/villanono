import streamlit as st

from components.page_config import set_page

set_page(st, False)

st.header("주소 검색")

col1, col2 = st.columns([3, 2])

with col1:
    st.text_input("찾고 싶은 장소를 입력하세요.", placeholder="거북골로 20길")

with col2:
    options = ["서대문구 북가좌동", "종로구 북가좌동", "강남구 북가좌동"]
    st.pills("지역 선택", options=options)
