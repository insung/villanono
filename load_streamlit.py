import pandas as pd
import plotly.express as px
import streamlit as st

df_all = pd.read_csv("data\\temp2\\all_2022_2024_서울특별시 서대문구 북가좌동.csv")
df_large = pd.read_csv("data\\temp2\\large_2022_2024_서울특별시 서대문구 북가좌동.csv")
df_medium = pd.read_csv(
    "data\\temp2\\medium_2022_2024_서울특별시 서대문구 북가좌동.csv"
)
df_small = pd.read_csv("data\\temp2\\small_2022_2024_서울특별시 서대문구 북가좌동.csv")

col1, col2, col3 = st.columns(3)

default_value = "거래량(건)"

choices = [
    "거래량(건)",
    "종합",
    "평균(만원)",
    "표준편차(만원)",
    "최소(만원)",
    "25%",
    "50%",
    "75%",
    "최대(만원)",
]

size_choices = ["전체", "소형(60미만)", "중형(80미만)", "대형(80이상)"]

with col1:
    size_selected = st.selectbox(
        label="선택:", options=size_choices, index=size_choices.index("전체")
    )

with col3:
    selected = st.selectbox(
        label="선택:", options=choices, index=choices.index(default_value)
    )

if size_selected == "전체":
    df = df_all
elif size_selected == "소형(60미만)":
    df = df_small
elif size_selected == "중형(80미만)":
    df = df_medium
else:
    df = df_large

df["계약년월"] = pd.to_datetime(df["계약년월"], format="%Y%m")
tickvals = df["계약년월"]
ticktext = df["계약년월"].dt.strftime("%Y-%m")

if selected == "종합":
    fig = px.line(df, x="계약년월", y="평균(만원)", markers=True)
    fig.update_xaxes(type="category", tickvals=tickvals, ticktext=ticktext)
    fig.add_scatter(
        x=df["계약년월"],
        y=df["최소(만원)"],
        mode="markers",
        name="최소",
        marker=dict(color="#E8E8E8", size=5),
        hoverinfo="none",
        showlegend=False,
    )
    fig.add_scatter(
        x=df["계약년월"],
        y=df["최대(만원)"],
        mode="markers",
        name="최대",
        marker=dict(color="#E8E8E8", size=5),
        hoverinfo="none",
        showlegend=False,
    )

    fig.update_traces(
        hovertemplate="<b>%{x}</b><br /><br />평균(만원): %{customdata[0]}<br />최소(만원): %{customdata[1]}<br />최대(만원): %{customdata[2]}",
        customdata=df[["평균(만원)", "최소(만원)", "최대(만원)"]].values,
    )
    st.plotly_chart(fig)
else:
    fig = px.line(df, x="계약년월", y=selected)
    fig.update_xaxes(type="category", tickvals=tickvals, ticktext=ticktext)
    # st.line_chart(df, x="계약년월", y=selected)
    st.plotly_chart(fig)


# df["계약년월"] = df["계약년월"].dt.strftime("%Y-%m")
# st.dataframe(df, hide_index=True)

st.write(df["계약년월"].min(), df["계약년월"].max())
print(type(df["계약년월"].min()))
