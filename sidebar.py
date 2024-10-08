import streamlit

__footer_style = """
<style>
.footer {
    position: fixed;
    bottom: 0;
    width: 100%;
    background-color: #f0f2f6;
    color: black;
    text-align: center;
    padding: 10px;
}
</style>
<div class='footer'>
    <p>😊 혹시 문의하실게 있으신가요? <a href="https://naver.me/Fjbv2rjB">여기</a>를 클릭하세요!</p>
</div>
"""


def add_sidebar(st: streamlit):
    st.sidebar.header("✨빌라 실거래 | 빌라 노노✨")
    st.sidebar.divider()
    st.sidebar.markdown(
        "이 사이트는 **국토교통부 실거래가 공개시스템**의 데이터로 만들어졌습니다. ([출처](https://rt.molit.go.kr/pt/xls/xls.do?mobileAt=))"
    )

    # Footer 추가
    st.sidebar.markdown(__footer_style, unsafe_allow_html=True)
