import streamlit

from components.map import get_si_gu_dong
from util import get_geocodes

SOUTH_KOREA_BOUNDS = [
    [33.0, 124.5],  # 남서쪽 (South-West)
    # [38.8, 130.0]   # 북동쪽 (North-East) - 울릉도 근처까지 (독도 제외 시)
    [38.8, 132.0],  # 북동쪽 (North-East) - 독도 포함 시
]

GEOBUK_GOL_RO = [37.577712, 126.914449]


def initialize(st: streamlit):
    # m = folium.Map(
    #     location=GEOBUK_GOL_RO,
    #     zoom_start=16,
    #     min_zoom=14,  # 이 값을 올려서 너무 축소되지 않도록 함
    #     max_zoom=18,
    #     min_lat=SOUTH_KOREA_BOUNDS[0][0],
    #     max_lat=SOUTH_KOREA_BOUNDS[1][0],
    #     min_lon=SOUTH_KOREA_BOUNDS[0][1],
    #     max_lon=SOUTH_KOREA_BOUNDS[1][1],
    #     control_scale=True,
    #     max_bounds=True,  # 여기에 경계 설정
    #     tiles="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png",
    #     attr="© CartoDB, OpenStreetMap contributors",
    # )

    # minimap = MiniMap(toggle_display=True)  # 접을 수 있는 MiniMap
    # minimap.add_to(m)

    # cluster = MarkerCluster().add_to(m)

    st.session_state.last_moved_center = GEOBUK_GOL_RO
    st.session_state.last_moved_si_gu_dong = get_si_gu_dong(GEOBUK_GOL_RO)

    si = st.session_state.last_moved_si_gu_dong[0]
    gu = st.session_state.last_moved_si_gu_dong[1]
    dong = st.session_state.last_moved_si_gu_dong[2]

    st.session_state.locations = get_geocodes(si, gu, dong)

    # for loc in st.session_state.locations:
    #     # popup = f"{loc['si']} {loc['gu']} {loc['dong']} ({loc['roadName']})"
    #     folium.CircleMarker(
    #         location=(loc["latitude"], loc["longitude"]),
    #         radius=6,
    #         color="crimson",
    #         fill=True,
    #         # popup=popup,
    #     ).add_to(cluster)

    # return m
