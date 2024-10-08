# IMPORT
import plotly.graph_objects as go
import plotly.graph_objs as go
import streamlit as st

fig = go.Figure()

# 데이터 추가
fig.add_trace(go.Scatter(x=[1, 2, 3], y=[4, 5, 6], mode="lines", name="Line 1"))

# 레이아웃 업데이트
fig.update_layout(
    title="My Plot Title",
    xaxis_title="X Axis Title",
    yaxis_title="Y Axis Title",
    legend=dict(
        itemsizing="constant",
        font=dict(size=12, color="blue"),
        bgcolor="LightSteelBlue",
        bordercolor="Black",
        borderwidth=2,
    ),
    xaxis=dict(
        title="X Axis Title",
        showgrid=True,
        zeroline=True,
        showline=True,
        gridcolor="LightPink",
        gridwidth=2,
        zerolinecolor="Red",
        zerolinewidth=4,
        linecolor="Black",
        linewidth=2,
    ),
    yaxis=dict(
        title="Y Axis Title",
        showgrid=True,
        zeroline=True,
        showline=True,
        gridcolor="LightPink",
        gridwidth=2,
        zerolinecolor="Red",
        zerolinewidth=4,
        linecolor="Black",
        linewidth=2,
    ),
    plot_bgcolor="rgba(0,0,0,0)",  # 투명 배경
    paper_bgcolor="LightSteelBlue",  # 전체 배경색
    hovermode="x unified",
)


st.plotly_chart(fig, use_container_width=True)
