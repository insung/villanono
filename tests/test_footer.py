import streamlit as st

# Footer HTML 및 CSS
footer_html = """
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #f1f1f1;
    color: black;
    text-align: center;
    padding: 10px;
}
</style>
<div class='footer'>
    <p>Developed with ❤️ by [Your Name]</p>
</div>
"""

# Footer 추가
st.markdown(footer_html, unsafe_allow_html=True)
