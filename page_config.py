import streamlit

from session_variables import init_session_variables


def set_page(st: streamlit, wide: bool):
    layout = "wide" if wide else "centered"
    st.set_page_config(
        page_title="빌라 실거래 검색은 빌라 노노",
        page_icon="🚀",
        layout=layout,
        # initial_sidebar_state="expanded",
    )

    init_session_variables(st)
