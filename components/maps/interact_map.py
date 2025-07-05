import folium
import streamlit
from folium.plugins import MarkerCluster, MiniMap
from geopy.geocoders import Nominatim

from components.map import SOUTH_KOREA_BOUNDS
from util import get_geocodes


def draw_map(st: streamlit, st_data) -> folium.Map:
    center = st.session_state.last_moved_center

    m = folium.Map(
        location=center,
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

    minimap = MiniMap(toggle_display=True)  # 접을 수 있는 MiniMap
    minimap.add_to(m)

    cluster = MarkerCluster().add_to(m)

    # 1) center 가 옮겨졌는지 확인
    # 2) 시, 구, 동이 바뀌었는지 확인
    if is_changed_center(st, st_data) and is_changed_region(
        st, st.session_state.last_moved_center
    ):
        si = st.session_state.last_moved_si_gu_dong[0]
        gu = st.session_state.last_moved_si_gu_dong[1]
        dong = st.session_state.last_moved_si_gu_dong[2]

        # road = location.raw["address"].get("road")
        # house_number = location.raw["address"].get("house_number")
        st.session_state.locations = get_geocodes(si, gu, dong)

    for loc in st.session_state.locations:
        # popup = f"{loc['si']} {loc['gu']} {loc['dong']} ({loc['roadName']})"
        folium.CircleMarker(
            location=(loc["latitude"], loc["longitude"]),
            radius=6,
            color="crimson",
            fill=True,
            # popup=popup,
        ).add_to(cluster)

    return m


def is_changed_center(st: streamlit, st_data) -> bool:
    if not st_data or not st_data.get("center"):
        return False

    center = st_data.get("center")

    if center != st.session_state.last_moved_center:
        coords = [center["lat"], center["lng"]]
        st.session_state.last_moved_center = coords
        return True

    return False


def is_changed_region(st: streamlit, query):
    if not st.session_state.last_moved_center:
        return False

    last_moved_si_gu_dong = reverse_by_query(query)

    if (
        last_moved_si_gu_dong
        and last_moved_si_gu_dong != st.session_state.last_moved_si_gu_dong
    ):
        st.session_state.last_moved_si_gu_dong = last_moved_si_gu_dong
        return True

    return False


def reverse_by_query(query: list) -> tuple | None:
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
