import streamlit as st

pages = [
    st.Page("🗺️메인페이지.py", title="메인 지도", icon="🗺️", default=True),
    # st.Page("pages/1_📈인사이트.py", title="인사이트 리포트", icon="📈"),
    # st.Page("pages/1_🧐통계_데이터.py", title="상세 통계 데이터", icon="🧐"),
]


pg = st.navigation(pages)
pg.run()
