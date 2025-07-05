import streamlit

from util import get_dong_options, get_geocodes, get_gu_options


def set_region_filter(st: streamlit):
    # 시
    selected_si = st.selectbox(
        label="",
        options=st.session_state.si_list,
        label_visibility="collapsed",
    )

    if st.session_state.selected_si != selected_si:
        st.session_state.selected_si = selected_si
        st.session_state.gu_list = get_gu_options(st.session_state.selected_si)
        st.session_state.selected_gu = st.session_state.gu_list[0]
        st.session_state.dong_list = get_dong_options(
            st.session_state.selected_si, st.session_state.selected_gu
        )
        st.session_state.selected_dong = st.session_state.dong_list[0]

    # 구
    selected_gu = st.selectbox(
        label="", options=st.session_state.gu_list, label_visibility="collapsed"
    )

    if st.session_state.selected_gu != selected_gu:
        st.session_state.selected_gu = selected_gu
        st.session_state.dong_list = get_dong_options(
            st.session_state.selected_si, st.session_state.selected_gu
        )
        st.session_state.selected_dong = st.session_state.dong_list[0]

    # 동
    st.session_state.selected_dong = st.selectbox(
        label="",
        options=st.session_state.dong_list,
        label_visibility="collapsed",
    )

    # 조회
    if st.button("조회"):
        st.session_state.locations = get_geocodes(
            st.session_state.selected_si,
            st.session_state.selected_gu,
            st.session_state.selected_dong,
        )
