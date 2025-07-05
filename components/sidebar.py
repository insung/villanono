import streamlit

from components.sidebars.compare_menu import set_compare_menu
from components.sidebars.detail_filter import set_detail_filter
from components.sidebars.region_filter import set_region_filter
from components.villa_info import set_villa_info


def set_sidebar(st: streamlit):
    # st.sidebar.header("🚀 빌라 실거래는 빌라 노노 🚀")

    with st.sidebar:
        with st.expander("지역 선택 필터", expanded=True, icon=":material/search:"):
            set_region_filter(st)

        with st.expander("상세 필터", expanded=False, icon=":material/visibility:"):
            set_detail_filter(st)

        with st.expander(
            "선택한 매물 정보", expanded=False, icon=":material/description:"
        ):
            set_villa_info(st)

        with st.expander(
            f"{st.session_state.selected_dong} 지역 비교",
            expanded=False,
            icon=":material/info:",
        ):
            set_compare_menu(st)
