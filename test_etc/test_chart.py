import pandas as pd
import plotly.express as px
import streamlit as st

# 데이터 생성
data = {
    "계약년월": ["202301", "202302", "202303", "202304", "202305"],
    "count": [30, 50, 36, 36, 36],
    "mean": [19346.67, 18141.60, 18582.92, 17666.67, 18062.50],
    "min": [6500, 4000, 7000, 2500, 9550],
    "max": [32000, 33000, 31500, 29000, 31000],
}

df = pd.DataFrame(data)

# Streamlit 앱
st.title("계약년월별 Count, Min, Max, Mean 값")

# Plotly를 사용하여 인터랙티브 차트 생성
fig = px.line(df, x="계약년월", y="count", markers=True, title="계약년월별 Count 값")
fig.add_scatter(
    x=df["계약년월"],
    y=df["min"],
    mode="markers",
    name="Min",
    marker=dict(color="green"),
)
fig.add_scatter(
    x=df["계약년월"], y=df["max"], mode="markers", name="Max", marker=dict(color="blue")
)
fig.add_scatter(
    x=df["계약년월"],
    y=df["mean"],
    mode="lines+markers",
    name="Mean",
    marker=dict(color="red"),
)

# Hover 데이터 추가
fig.update_traces(
    hovertemplate="<b>%{x}</b><br>Count: %{y}<br>Mean: %{customdata[0]}",
    customdata=df[["mean"]].values,
)

# Streamlit에서 차트 표시
st.plotly_chart(fig)
