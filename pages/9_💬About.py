import streamlit as st

from page_config import set_page
from sidebar import set_sidebar

#### page config ####
set_page(st, False)

#### sidebar ####
set_sidebar(st)

st.info(
    "이 사이트는 **국토교통부 실거래가 공개시스템**의 데이터로 만들어졌습니다. ([출처](https://rt.molit.go.kr/pt/xls/xls.do?mobileAt=))"
)

st.markdown("""
### 🩺 이 사이트를 만든 배경

아파트 실거래는 찾기 쉬운데, 빌라 실거래는 발견할 수 없어 만들어보았습니다.
공공데이터를 이용하여 집계된 데이터를 분석하여 인사이트를 얻을 수 있을 것입니다.
아직 베타 버전이라 많은 기능은 없지만 계속해서 업데이트할 예정입니다. 🔥🔥🔥""")

st.divider()
st.markdown("""
### 😘 이런분께 추천해요!

- 빌라 시장에 대한 인사이트가 필요하신 분
- 아파트는 비싸 부담스럽고 주위에서 빌라는 사면 안된다고 하여 망설이는 분
- 영끌없이 자산 시장에 진입하고 싶으신 분
- 빌라 투자에 망설이는 분
- 빌라 전세 사기 때문에 빌라 전세 살기에 망설이는 분
""")

st.divider()
st.markdown("""
### 🧑‍💻 개발 스토리

- 24시간 만에 (아이와 놀면서) 빌라 실거래가 분석 사이트 구축 ([링크](https://open.substack.com/pub/imissyoubrad/p/24?r=4gagwz&utm_campaign=post&utm_medium=web&showWelcomeOnShare=true))
""")
