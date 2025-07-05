import streamlit

from util import get_geocodes


def user_interaction_map(st: streamlit, st_data):
    if not st_data:
        return

    # if is_changed_center(st, st_data):
    #     center = (st_data["center"]["lat"], st_data["center"]["lng"])
    #     st.session_state.last_moved_center = center

    # last_moved_si_gu_dong = get_si_gu_dong(center)
    # if last_moved_si_gu_dong != st.session_state.last_moved_si_gu_dong:
    #     set_si_gu_dong(st, last_moved_si_gu_dong)


def set_si_gu_dong(st: streamlit, last_moved_si_gu_dong: tuple):
    st.session_state.last_moved_si_gu_dong = last_moved_si_gu_dong

    si = st.session_state.last_moved_si_gu_dong.item1
    gu = st.session_state.last_moved_si_gu_dong.item2
    dong = st.session_state.last_moved_si_gu_dong.item3

    st.session_state.locations = get_geocodes(si, gu, dong)
