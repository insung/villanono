from math import ceil

import numpy as np
import pandas as pd
import streamlit as st

# 예시 데이터프레임 생성
df = pd.DataFrame(
    {"Column 1": np.arange(1, 101), "Column 2": np.random.randint(1, 100, 100)}
)

# 페이지 크기 설정
page_size = 10

# 페이지 번호 입력
page_number = st.number_input(
    label="Page Number",
    min_value=1,
    max_value=ceil(len(df) / page_size),
    step=1,
    value=1,
)

# 현재 페이지의 시작과 끝 인덱스 계산
current_start = (page_number - 1) * page_size
current_end = page_number * page_size

# 현재 페이지의 데이터프레임 슬라이스
current_df = df.iloc[current_start:current_end]

# 데이터프레임 표시
st.dataframe(current_df, use_container_width=True)
