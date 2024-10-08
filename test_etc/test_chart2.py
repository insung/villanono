import pandas as pd
import plotly.graph_objects as go

# 데이터 생성
data = {"date": ["202401", "202402", "202403"], "value": [4, float("nan"), 5]}

# 데이터프레임 생성
df = pd.DataFrame(data)

# 날짜 형식 변환
df["date"] = pd.to_datetime(df["date"], format="%Y%m")

# NaN 값을 "데이터 없음"으로 대체
df["value"] = df["value"].fillna("데이터 없음")

# 오늘 날짜 추가
today = pd.to_datetime("2024-10-02")
new_row = pd.DataFrame({"date": [today], "value": [df["value"].iloc[-1]]})
df = pd.concat([df, new_row], ignore_index=True)

# 라인 차트 생성
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=df["date"],
        y=df["value"],
        mode="lines+markers+text",
        text=df["value"],
        name="Value",
    )
)

# 레이아웃 설정
fig.update_layout(
    title="Time Series Line Chart", xaxis_title="Date", yaxis_title="Value"
)

# 차트 출력
fig.show()
