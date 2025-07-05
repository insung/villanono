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
from util import get_dong_options, get_geocodes, get_gu_options

set_page(st, wide=True, sidebar_expand=True)


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


# Sidebar
with st.sidebar:
    with st.expander("지역 선택 필터", expanded=True, icon=":material/search:"):
        # 시
        selected_si = st.selectbox(
            label="",
            options=st.session_state.si_list,
            label_visibility="collapsed",
            key="selectbox_si",
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
            key="selectbox_gu",
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
            key="selectbox_dong",
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

# 캐시된 기본 지도 객체 가져오기
base_map_obj = build_base_map_cached()

# 동적으로 마커를 추가하기 위한 새로운 folium.Map 객체 생성
# 캐시된 base_map_obj를 직접 수정하지 않기 위해 속성을 복사하여 새 객체를 만듭니다.
map_to_render = copy.deepcopy(base_map_obj)

# 새로운 지도 객체에 고정 플러그인 다시 추가 (캐시된 지도에서 복사)
# map_to_render.add_child(MeasureControl())
# minimap = MiniMap(toggle_display=True)
# minimap.add_to(map_to_render)

# 현재 세션 상태의 위치 정보(locations)를 기반으로 동적 마커 추가
locs = st.session_state.get("locations", [])
if locs:  # locations 데이터가 있을 경우에만 마커 추가
    marker_cluster = MarkerCluster().add_to(map_to_render)  # 마커 클러스터 생성
    for loc in locs:
        lat, lng = loc.get("latitude"), loc.get("longitude")
        if lat is not None and lng is not None:
            # 팝업 내용 구성 (더 자세한 정보 포함 가능)
            # popup_content = f"<b>{loc.get('si', '')} {loc.get('gu', '')} {loc.get('dong', '')}</b><br>" \
            #                 f"도로명: {loc.get('roadName', '')}<br>" \
            #                 f"위도: {lat:.4f}, 경도: {lng:.4f}"
            folium.CircleMarker(
                location=(lat, lng),
                radius=6,  # 마커 크기
                color="crimson",  # 테두리 색상
                fill=True,
                fill_color="crimson",  # 채우기 색상
                fill_opacity=0.7,  # 채우기 투명도
                # popup=folium.Popup(popup_content, max_width=300), # 팝업 내용 및 최대 너비
                tooltip=f"{loc.get('dong', '')} 위치",  # 마우스 오버 시 툴팁
            ).add_to(marker_cluster)


# st_folium을 사용하여 지도 렌더링
# 중요:
# - returned_obj=None: 지도를 움직일 때마다 Streamlit 앱이 불필요하게 재실행되는 것을 방지합니다.
# - key: 지도 컴포넌트의 고유 식별자를 제공합니다. 이 키가 변경되면 지도가 다시 그려집니다.
#   여기서는 locations의 길이와 선택된 시/구/동을 조합하여 키를 생성하여,
#   검색 결과나 지역 선택이 변경될 때만 지도가 업데이트되도록 합니다.
map_data = st_folium(
    map_to_render,
    width="100%",  # 지도의 너비를 100%로 설정
    # returned_objects=None,
    key=f"folium_map_{len(locs)}_{st.session_state.selected_si}_{st.session_state.selected_gu}_{st.session_state.selected_dong}",  # 동적 키
)
