import pandas as pd
import streamlit as st

df = pd.read_csv("test44.csv", skiprows=1)
df2 = df[["Unnamed: 1", "count", "mean", "std", "min", "25%", "50%", "75%", "max"]]

df_options = [
    "계약년월",
    "계약건수",
    "평균(만원)",
    "표준편차(만원)",
    "최소가격(만원)",
    "25%",
    "50%",
    "75%",
    "최대(만원)",
]
df2.columns = df_options
df2["계약년월"] = df2["계약년월"].astype(str)

# meanDF = df2[["계약년월", "mean"]]

col1, col2, col3 = st.columns(3)

default_value = "계약건수"

choices = [
    "계약건수",
    "평균(만원)",
    "표준편차(만원)",
    "최소가격(만원)",
    "25%",
    "50%",
    "75%",
    "최대(만원)",
]

with col3:
    selected = st.selectbox(
        label="선택:", options=choices, index=choices.index(default_value)
    )

st.line_chart(df2, x="계약년월", y=selected)
