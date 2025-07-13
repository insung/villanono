import copy

import folium
import streamlit as st
from folium.plugins import MarkerCluster, MeasureControl, MiniMap
from streamlit_folium import st_folium

from components.map_variables import GEOBUK_GOL_RO, MAIN_PAGE_STYLE, SOUTH_KOREA_BOUNDS
from components.page_config import set_page
from components.sidebars.compare_menu import set_compare_menu
from components.sidebars.detail_filter import set_detail_filter
from components.villa_info import set_villa_info
from util import (
    get_dong_options,
    get_geocodes,
    get_gu_options,
    get_si_gu_dong_from_coords,
)


def update_filters_from_map():
    """현재 지도 중심 지역으로 사이드바 필터를 업데이트합니다."""
    center = st.session_state.get("last_moved_center")
    if not center:
        return

    new_address = get_si_gu_dong_from_coords(center)
    if not new_address:
        return

    new_si, new_gu, new_dong = new_address

    # 가드 절(Guard Clause) 패턴으로 가독성 개선
    if new_si not in st.session_state.si_list:
        return
    st.session_state.selected_si = new_si
    st.session_state.gu_list = get_gu_options(new_si)

    if new_gu not in st.session_state.gu_list:
        return
    st.session_state.selected_gu = new_gu
    st.session_state.dong_list = get_dong_options(new_si, new_gu)

    # '동' 선택 로직
    if new_dong in st.session_state.dong_list:
        st.session_state.selected_dong = new_dong
    elif st.session_state.dong_list:
        st.session_state.selected_dong = st.session_state.dong_list[0]
    else:
        st.session_state.selected_dong = None


set_page(st, wide=True, sidebar_expand=True)

# 지도 이동에 따른 필터 업데이트 처리
# 위젯이 렌더링되기 전에 상태를 변경해야 StreamlitAPIException을 피할 수 있습니다.
if st.session_state.get("update_filters_from_map_flag", False):
    st.session_state.update_filters_from_map_flag = (
        False  # 플래그를 즉시 리셋하여 무한 루프 방지
    )
    update_filters_from_map()


# Main Page Sytle
st.markdown(
    MAIN_PAGE_STYLE,
    unsafe_allow_html=True,
)


@st.cache_resource
def build_base_map_cached() -> folium.Map:
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
    return m


def on_si_change():
    """'시' 선택이 변경되면 '구'와 '동' 목록을 연쇄적으로 업데이트합니다."""
    st.session_state.gu_list = get_gu_options(st.session_state.selected_si)
    if st.session_state.gu_list:
        st.session_state.selected_gu = st.session_state.gu_list[0]
        on_gu_change()  # '구'가 변경되었으므로 '동' 목록도 업데이트
    else:
        st.session_state.selected_gu = None
        st.session_state.dong_list = []
        st.session_state.selected_dong = None


def on_gu_change():
    """'구' 선택이 변경되면 '동' 목록을 업데이트합니다."""
    if st.session_state.selected_gu:
        st.session_state.dong_list = get_dong_options(
            st.session_state.selected_si, st.session_state.selected_gu
        )
        if st.session_state.dong_list:
            st.session_state.selected_dong = st.session_state.dong_list[0]
        else:
            st.session_state.selected_dong = None
    else:
        st.session_state.dong_list = []
        st.session_state.selected_dong = None


def on_dong_change():
    """'동' 선택이 변경되면 조회 버튼을 활성화합니다."""
    pass


# Sidebar
with st.sidebar:
    with st.expander("지역 선택 필터", expanded=True, icon=":material/search:"):
        # 시
        st.selectbox(
            label="시",
            options=st.session_state.si_list,
            key="selected_si",
            on_change=on_si_change,
        )

        # 구
        st.selectbox(
            label="구",
            options=st.session_state.gu_list,
            key="selected_gu",
            on_change=on_gu_change,
            disabled=not st.session_state.gu_list,
        )

        # 동
        st.selectbox(
            label="동",
            options=st.session_state.dong_list,
            key="selected_dong",
            on_change=on_dong_change,
            disabled=not st.session_state.dong_list,
        )

        # 조회
        if st.button("조회"):
            # 필터 값으로 검색 실행
            locations = get_geocodes(
                st.session_state.selected_si,
                st.session_state.selected_gu,
                st.session_state.selected_dong,
            )
            st.session_state.locations = locations
            # 마지막 검색 주소 업데이트
            st.session_state.last_searched_address = (
                st.session_state.selected_si,
                st.session_state.selected_gu,
                st.session_state.selected_dong,
            )
            st.rerun()

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

    # st.divider()
    # st.page_link("pages/1_📈인사이트.py", label="인사이트", icon="📈")


def add_location_markers(folium_map: folium.Map, locations: list):
    """주어진 위치 목록을 기반으로 Folium 지도에 마커를 추가합니다."""
    if not locations:
        return

    marker_cluster = MarkerCluster().add_to(folium_map)
    for loc in locations:
        lat, lng = loc.get("latitude"), loc.get("longitude")
        if lat is not None and lng is not None:
            folium.CircleMarker(
                location=(lat, lng),
                radius=6,
                color="crimson",
                fill=True,
                fill_color="crimson",
                fill_opacity=0.7,
                tooltip=f"{loc.get('dong', '')} 위치",
            ).add_to(marker_cluster)


# 캐시된 기본 지도 객체 가져오기
base_map_obj = build_base_map_cached()

# 동적으로 마커를 추가하기 위한 새로운 folium.Map 객체 생성
# 캐시된 base_map_obj를 직접 수정하지 않기 위해 속성을 복사하여 새 객체를 만듭니다.
map_to_render = copy.deepcopy(base_map_obj)

# 마지막으로 사용자가 움직인 위치로 지도 중심을 업데이트합니다.
if st.session_state.get("last_moved_center"):
    map_to_render.location = st.session_state.last_moved_center

# 새로운 지도 객체에 고정 플러그인 다시 추가 (캐시된 지도에서 복사)
# map_to_render.add_child(MeasureControl())
# minimap = MiniMap(toggle_display=True)
# minimap.add_to(map_to_render)

locations = st.session_state.get("locations", [])
add_location_markers(map_to_render, locations)

# st_folium을 사용하여 지도 렌더링
# 중요:
# - returned_obj=None: 지도를 움직일 때마다 Streamlit 앱이 불필요하게 재실행되는 것을 방지합니다.
# - key: 지도 컴포넌트의 고유 식별자를 제공합니다. 이 키가 변경되면 지도가 다시 그려집니다.
#   여기서는 locations의 길이와 선택된 시/구/동을 조합하여 키를 생성하여,
#   검색 결과나 지역 선택이 변경될 때만 지도가 업데이트되도록 합니다.
map_data = st_folium(
    map_to_render,
    width="100%",
    key=f"folium_map_{len(locations)}_{st.session_state.selected_si}_{st.session_state.selected_gu}_{st.session_state.selected_dong}",  # 동적 키
)

# --- 2-B 단계: 지도 상호작용 로직 ---
if map_data and map_data.get("bounds") and map_data.get("center"):
    current_bounds = map_data["bounds"]
    last_bounds = st.session_state.get("last_bounds")

    # 지도 경계가 변경되었을 때만 로직 실행 (불필요한 API 호출 방지)
    if current_bounds != last_bounds:
        st.session_state.last_bounds = current_bounds

        current_center = (map_data["center"]["lat"], map_data["center"]["lng"])
        st.session_state.last_moved_center = current_center

        # 현재 지도 중심의 주소 가져오기
        current_address = get_si_gu_dong_from_coords(current_center)

        if current_address and st.session_state.last_searched_address:
            # 현재 주소와 마지막 검색 주소가 다르면 버튼 표시
            if current_address != st.session_state.last_searched_address:
                # 필터 업데이트 플래그를 설정하고 페이지를 새로고침하여 UI에 반영합니다.
                st.session_state.update_filters_from_map_flag = True
                st.rerun()
