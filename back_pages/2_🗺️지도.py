import folium
import streamlit as st
from folium.plugins import MarkerCluster, MeasureControl, MiniMap

# 주소 변환(Reverse Geocoding) 예시: geopy 사용
from streamlit_folium import st_folium

from page_config import set_page

# from topbar import add_topbar

SOUTH_KOREA_BOUNDS = [
    [33.0, 124.5],  # 남서쪽 (South-West)
    # [38.8, 130.0]   # 북동쪽 (North-East) - 울릉도 근처까지 (독도 제외 시)
    [38.8, 132.0],  # 북동쪽 (North-East) - 독도 포함 시
]

geobuk_gol_ro = [37.577712, 126.914449]

set_page(st, wide=True, sidebar_expand=False)


#### topbar ####
# add_topbar(st)

if "last_center" not in st.session_state:
    st.session_state.last_center = None

if "last_si_gu_dong" not in st.session_state:
    st.session_state.last_si_gu_dong = None


def draw_map(center=None, locations=None):
    m = folium.Map(
        location=center or geobuk_gol_ro,
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

    # 마커 먼저 붙임
    if locations:
        for loc in locations:
            # popup = f"{loc['si']} {loc['gu']} {loc['dong']} ({loc['roadName']})"
            folium.CircleMarker(
                location=(loc["latitude"], loc["longitude"]),
                radius=6,
                color="crimson",
                fill=True,
                # popup=popup,
            ).add_to(cluster)

    return st_folium(m, width="100%")


# 최초 또는 상태 변경 시마다 지도 그리기

st_data = draw_map(
    center=st.session_state.last_center,
    locations=st.session_state.get("locations"),
)

# 유저 인터랙션 처리

# if st_data and st_data.get("center"):
#     ne = st_data["bounds"]["_northEast"]
#     sw = st_data["bounds"]["_southWest"]

#     center = (st_data["center"]["lat"], st_data["center"]["lng"])
#     if center != st.session_state.last_center:
#         st.session_state.last_center = center

#     # st.info(
#     #     f"클릭한 위치: 위도 {center_lat:.6f}, 경도 {center_lon:.6f} / bounds NE: {ne['lat']:.6f}, {ne['lng']:.6f} / bounds SW: {sw['lat']:.6f}, {sw['lng']:.6f}"
#     # )

#     geo = Nominatim(user_agent="villanono").reverse(center, language="ko")

#     if geo and geo.raw.get("address"):
#         addr = geo.raw["address"]
#         si = addr.get("city", addr.get("state", ""))
#         gu = addr.get("borough", addr.get("county", ""))
#         dong = addr.get("quarter", addr.get("suburb", ""))

#         last_si_gu_dong = (si, gu, dong)

#         if last_si_gu_dong != st.session_state.last_si_gu_dong:
#             st.session_state.last_si_gu_dong = last_si_gu_dong

#             # road = location.raw["address"].get("road")
#             # house_number = location.raw["address"].get("house_number")
#             # st.write(f"주소: {si} {gu} {road} {house_number}")

#             # 마커 추가
#             # selected_si = st.session_state["selected_si"]
#             # selected_gu = st.session_state["selected_gu"]
#             # selected_dong = st.session_state["selected_dong"]
#             st.session_state.locations = get_geocodes(si, gu, dong)
#             # roadName = st.text_input("도로명 입력", locations)
#             # st.experimental_rerun()
#             st_data = draw_map(
#                 center=st.session_state.last_center,
#                 locations=st.session_state.get("locations"),
#             )
#     else:
#         st.session_state.locations = []
