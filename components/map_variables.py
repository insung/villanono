SOUTH_KOREA_BOUNDS = [
    [33.0, 124.5],  # 남서쪽 (South-West)
    # [38.8, 130.0]   # 북동쪽 (North-East) - 울릉도 근처까지 (독도 제외 시)
    [38.8, 132.0],  # 북동쪽 (North-East) - 독도 포함 시
]

GEOBUK_GOL_RO = [37.577712, 126.914449]


MAIN_PAGE_STYLE = """
<style>
    /* 헤더(로고, 앱명 영역) 숨기기 */
    header.stAppHeader[data-testid="stHeader"] {
        display: none !important;
    }
    /* 툴바(Deploy/Share/메뉴 버튼 그룹) 숨기기 */
    div[data-testid="stToolbar"] {
        display: none !important;
    }

    /* 사이드바를 축소하는 버튼(<)을 숨깁니다. */
    div[data-testid="stSidebarCollapseButton"] {
        margin-top: -100px !important;
    }

    /* 여백만 남아 있을 경우 빈 공간도 제거 */
    .stApp .main {
        padding-top: 0 !important;
    }

    /* stMainBlockContainer + block-container 조합을 타겟팅 */
    div.stMainBlockContainer.block-container {
        padding-top: 10px !important;
    }

    /* 페이지 레이아웃 패딩/마진 제거 */
    .block-container {
        padding-left: 5px !important;
        padding-right: 4px !important;
        padding-bottom: 10px !important;
        overflow: visible !important;
    }

    /* folium-map 컨테이너 여백 제거 */
    .folium-map,
    .folium-map .leaflet-container {
        margin-bottom: 0 !important;
        padding-bottom: 0 !important;
    }

    /* st_folium 이 만드는 iframe 여백 제거 */
    .streamlit-embedded-widget .folium-map > iframe {
        margin-bottom: 0 !important;
        padding-bottom: 0 !important;
    }

    /* body 자체도 스크롤 사라지게(선택) */
    body {
        overflow-y: hidden !important;
    }
</style>
"""


STYLE_BACKUP = """
    /* 앱 전체 배경색 */
    .stApp {
        background-color: #282C34 !important;
    }
    /* 본문 영역(block-container)도 같은 색으로 */
    .stApp .block-container {
        background-color: #282C34 !important;
    }

    /* 헤더 영역 */
    header.stAppHeader[data-testid="stHeader"] {
        background-color: #282C34 !important;
    }
"""
