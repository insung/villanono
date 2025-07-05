import folium
import streamlit as st
from folium.plugins import MarkerCluster, MeasureControl, MiniMap
from streamlit_folium import st_folium

from components.map_variables import GEOBUK_GOL_RO, MAIN_PAGE_STYLE, SOUTH_KOREA_BOUNDS
from components.page_config import set_page
from components.sidebars.compare_menu import set_compare_menu
from components.sidebars.detail_filter import set_detail_filter
from components.villa_info import set_villa_info
from util import get_dong_options, get_geocodes, get_gu_options

set_page(st, wide=True, sidebar_expand=True)


# Main Page Sytle
st.markdown(
    MAIN_PAGE_STYLE,
    unsafe_allow_html=True,
)


@st.cache_resource
def build_base_map(locations: tuple[tuple[float, float], ...]) -> folium.Map:
    m = folium.Map(
        location=GEOBUK_GOL_RO,
        zoom_start=16,
        min_zoom=14,  # 이 값을 올려서 너무 축소되지 않도록 함
        max_zoom=18,
        min_lat=SOUTH_KOREA_BOUNDS[0][0],
        max_lat=SOUTH_KOREA_BOUNDS[1][0],
        min_lon=SOUTH_KOREA_BOUNDS[0][1],
        max_lon=SOUTH_KOREA_BOUNDS[1][1],
        control_scale=True,
        max_bounds=True,  # 여기에 경계 설정
        tiles="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png",
        attr="© CartoDB, OpenStreetMap contributors",
    )

    m.add_child(MeasureControl())
    # folium.plugins.Geocoder().add_to(m)
    # folium.plugins.LocateControl(auto_start=True).add_to(m)

    minimap = MiniMap(toggle_display=True)  # 접을 수 있는 MiniMap
    minimap.add_to(m)

    cluster = MarkerCluster().add_to(m)

    for lat, lng in locations:
        # if not loc["latitude"] or not loc["longitude"]:
        #     pass

        if not lat or not lng:
            pass

        # popup = f"{loc['si']} {loc['gu']} {loc['dong']} ({loc['roadName']})"
        folium.CircleMarker(
            # location=(loc["latitude"], loc["longitude"]),
            location=(lat, lng),
            radius=6,
            color="crimson",
            fill=True,
            # popup=popup,
        ).add_to(cluster)

    return m


# Sidebar
with st.sidebar:
    with st.expander("지역 선택 필터", expanded=True, icon=":material/search:"):
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
            label="",
            options=st.session_state.gu_list,
            label_visibility="collapsed",
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

    with st.expander("상세 필터", expanded=False, icon=":material/visibility:"):
        set_detail_filter(st)

    with st.expander("선택한 매물 정보", expanded=False, icon=":material/description:"):
        set_villa_info(st)

    with st.expander(
        f"{st.session_state.selected_dong} 지역 비교",
        expanded=False,
        icon=":material/info:",
    ):
        set_compare_menu(st)

locs = st.session_state.get("locations", [])
coords = tuple((loc["latitude"], loc["longitude"]) for loc in locs if loc["latitude"])
map_obj = build_base_map(coords)

st_folium(map_obj, width="100%")
