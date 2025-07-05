import streamlit

from components.session_variables import init_session_variables


def set_page(st: streamlit, wide: bool, sidebar_expand: bool = True):
    layout = "wide" if wide else "centered"
    sidebar_option = "expanded" if sidebar_expand else "collapsed"
    st.set_page_config(
        page_title="빌라 실거래 검색은 빌라 노노",
        page_icon="🚀",
        layout=layout,
        initial_sidebar_state=sidebar_option,
        menu_items=None,
    )

    init_session_variables(st)
