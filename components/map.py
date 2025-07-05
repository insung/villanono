import folium
import streamlit
from folium.plugins import MarkerCluster, MeasureControl, MiniMap
from geopy.geocoders import Nominatim
from streamlit_folium import st_folium

from util import get_geocodes

SOUTH_KOREA_BOUNDS = [
    [33.0, 124.5],  # 남서쪽 (South-West)
    # [38.8, 130.0]   # 북동쪽 (North-East) - 울릉도 근처까지 (독도 제외 시)
    [38.8, 132.0],  # 북동쪽 (North-East) - 독도 포함 시
]

GEOBUK_GOL_RO = [37.577712, 126.914449]


def draw_map(st: streamlit):
    # 처음 접속하여 last center 가 없는 경우
    if st.session_state.last_moved_center is None:
        st.session_state.last_moved_center = GEOBUK_GOL_RO

    m = folium.Map(
        location=st.session_state.last_moved_center,
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
    if st.session_state.locations is None:
        last_moved_si_gu_dong = get_si_gu_dong(st.session_state.last_moved_center)

        st.session_state.last_moved_si_gu_dong = last_moved_si_gu_dong

        si = st.session_state.last_moved_si_gu_dong[0]
        gu = st.session_state.last_moved_si_gu_dong[1]
        dong = st.session_state.last_moved_si_gu_dong[2]

        st.session_state.locations = get_geocodes(si, gu, dong)

    if st.session_state.locations:
        for loc in st.session_state.locations:
            # popup = f"{loc['si']} {loc['gu']} {loc['dong']} ({loc['roadName']})"
            folium.CircleMarker(
                location=(loc["latitude"], loc["longitude"]),
                radius=6,
                color="crimson",
                fill=True,
                # popup=popup,
            ).add_to(cluster)

    return st_folium(m, width="100%")


def get_si_gu_dong(query) -> tuple | None:
    if not query:
        return None

    geo = Nominatim(user_agent="villanono").reverse(query, language="ko")

    if geo and geo.raw.get("address"):
        addr = geo.raw["address"]
        si = addr.get("city", addr.get("state", ""))
        gu = addr.get("borough", addr.get("county", ""))
        dong = addr.get("quarter", addr.get("suburb", ""))

        return (si, gu, dong)

    return None
