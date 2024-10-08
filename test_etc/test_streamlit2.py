import pandas as pd
import streamlit as st

# 데이터프레임 생성
data = {
    "계약년월": ["202204", "202206", "202212"],
    "거래량(건)": [1, 1, 1],
    "평균(만원)": [43000.0, 46000.0, 53000.0],
    "표준편차(만원)": [None, None, None],
    "최소(만원)": [43000, 46000, 53000],
    "25%": [43000.0, 46000.0, 53000.0],
    "50%": [43000.0, 46000.0, 53000.0],
    "75%": [43000.0, 46000.0, 53000.0],
    "최대(만원)": [43000, 46000, 53000],
}
df = pd.DataFrame(data)

# 계약년월을 datetime 형식으로 변환
df["계약년월"] = pd.to_datetime(df["계약년월"], format="%Y%m")

# 슬라이더 생성
start_date, end_date = st.slider(
    "계약년월 범위 선택",
    min_value=df["계약년월"].min().to_pydatetime(),
    max_value=df["계약년월"].max().to_pydatetime(),
    value=(df["계약년월"].min().to_pydatetime(), df["계약년월"].max().to_pydatetime()),
    format="YYYY-MM",
)

# 선택된 범위에 해당하는 데이터 필터링
filtered_df = df[
    (df["계약년월"] >= pd.to_datetime(start_date))
    & (df["계약년월"] <= pd.to_datetime(end_date))
]

# 데이터프레임 표시
st.dataframe(filtered_df)
