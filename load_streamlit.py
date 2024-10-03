import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="빌라 노노 | 베타버전",
    page_icon="🚀",
    # layout="wide",
    # initial_sidebar_state="expanded",
)

st.header("안녕하세요! 빌라 노노입니다. ✨")
st.error(
    "이 사이트의 데이터는 국토교통부 실거래가 공개시스템의 연립/다세대 데이터를 토대로 만들어졌습니다. ([출처](https://rt.molit.go.kr/pt/xls/xls.do?mobileAt=))"
)
st.success(
    "서울시 서대문구 북가좌동 2022년 1월 1일 부터 2024년 10월 1일까지의 실거래 매매 정보입니다. 계속해서 업데이트할 예정입니다.",
    icon="🔥",
)
st.divider()

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

size_choices = ["전체", "소형(60㎡미만)", "중형(80㎡미만)", "대형(80㎡이상)"]

with col1:
    size_selected = st.selectbox(
        label="면적:", options=size_choices, index=size_choices.index("전체")
    )

with col3:
    selected = st.selectbox(
        label="지표:", options=choices, index=choices.index(default_value)
    )

if size_selected == "전체":
    df = df_all
elif size_selected == "소형(60㎡미만)":
    df = df_small
elif size_selected == "중형(80㎡미만)":
    df = df_medium
else:
    df = df_large

df["계약년월"] = pd.to_datetime(df["계약년월"], format="%Y%m")
tickvals = df["계약년월"]
ticktext = df["계약년월"].dt.strftime("%Y-%m")

if selected == "종합":
    fig = px.line(df, x="계약년월", y="평균(만원)", markers=True)
    fig.update_xaxes(type="category", tickvals=tickvals, ticktext=ticktext)
    fig.update_yaxes(tickformat=",.0f")
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
        hovertemplate="<b>%{x}</b><br /><br />평균(만원): %{customdata[0]:,.0f}<br />최소(만원): %{customdata[1]:,.0f}<br />최대(만원): %{customdata[2]:,.0f}",
        customdata=df[["평균(만원)", "최소(만원)", "최대(만원)"]].values,
    )
    st.plotly_chart(fig)
else:
    fig = px.line(df, x="계약년월", y=selected)
    fig.update_xaxes(type="category", tickvals=tickvals, ticktext=ticktext)
    fig.update_yaxes(tickformat=",.0f")
    # st.line_chart(df, x="계약년월", y=selected)
    st.plotly_chart(fig)


# df["계약년월"] = df["계약년월"].dt.strftime("%Y-%m")
# st.dataframe(df, hide_index=True)

# st.write(df["계약년월"].min(), df["계약년월"].max())
# print(type(df["계약년월"].min()))

st.divider()

st.info("혹시 문의하실게 있으신가요? [여기](https://naver.me/Fjbv2rjB)를 클릭하세요!")
