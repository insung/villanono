import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

# 예제 데이터프레임 생성
df = pd.DataFrame(
    {
        "date": pd.date_range(start="1/1/2020", periods=100),
        "price": range(100, 200),
        "volume": range(200, 300),
    }
)

# 서브플롯 생성 (가격 차트: 70%, 거래량 차트: 30%)
fig = make_subplots(
    rows=2,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.1,
    row_heights=[0.7, 0.3],
    subplot_titles=("Price", "Volume"),
)

# 가격 라인 차트 추가
fig.add_trace(go.Scatter(x=df["date"], y=df["price"], name="Price"), row=1, col=1)

# 거래량 바 차트 추가
fig.add_trace(go.Bar(x=df["date"], y=df["volume"], name="Volume"), row=2, col=1)

# 레이아웃 업데이트
fig.update_layout(height=600, showlegend=False)

# Streamlit에 차트 표시
st.plotly_chart(fig, use_container_width=True)
