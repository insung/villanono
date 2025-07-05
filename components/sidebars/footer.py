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


def set_footer(st: streamlit):
    # Footer 추가
    st.sidebar.markdown(__footer_style, unsafe_allow_html=True)
