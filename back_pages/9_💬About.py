import streamlit as st
from sidebar import set_sidebar

from components.page_config import set_page

#### page config ####
set_page(st, False)

#### sidebar ####
set_sidebar(st)

st.snow()

st.info(
    "이 사이트는 **국토교통부 실거래가 공개시스템**의 데이터로 만들어졌습니다. ([출처](https://rt.molit.go.kr/pt/xls/xls.do?mobileAt=))"
)
st.success("매매 실거래는 2006년 1월 1일 부터 2024년 10월 31일까지의 정보입니다.")
st.success("전세 실거래는 2011년 1월 1일 부터 2024년 10월 31일까지의 정보입니다.")

st.divider()
st.markdown("""
### 🩺 이 사이트를 만든 배경

아파트 실거래는 찾기 쉬운데, 빌라 실거래는 찾을 수가 없어 직접 만들어보았습니다.
공공데이터를 이용하여 수집된 데이터를 분석하여 제공하니 인사이트를 얻을 수 있을 것입니다.
아직 베타 버전이라 많은 기능은 없지만 계속해서 업데이트할 예정입니다. 🔥🔥🔥""")

st.divider()
st.markdown("""
### 😘 이런분께 추천해요!

- 빌라 시장에 대한 인사이트가 필요하신 분
- 아파트 매매, 전세는 비싸 부담스러운 분
- 영끌없이 자산 시장에 진입하고 싶으신 분
- 주위에서 빌라는 사면 안된다고 하여 망설이는 분
- 빌라 시장에 대한 실거래 자료가 없어 망설이는 분
- 빌라 전세 사기 때문에 살아도 될까 망설이는 분
""")

st.divider()
st.markdown("""
### 🧑‍💻 개발 스토리

- 24시간 만에 (아이와 놀면서) 빌라 실거래가 분석 사이트 구축 ([링크](https://open.substack.com/pub/imissyoubrad/p/24?r=4gagwz&utm_campaign=post&utm_medium=web&showWelcomeOnShare=true))
""")

st.divider()
st.markdown("""            
### 🤩 About Me

- 오래전 만든 [Github 페이지 가기](https://insung.github.io/) 🙈
""")
