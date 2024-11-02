import pandas as pd
import streamlit as st
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
)


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    modify = st.checkbox("Add filters")
    if not modify:
        return df

    df = df.copy()

    for col in df.columns:
        if is_categorical_dtype(df[col]) or df[col].nunique() < 10:
            user_input = st.multiselect(
                f"Filter {col}", df[col].unique(), default=list(df[col].unique())
            )
            df = df[df[col].isin(user_input)]
        elif is_numeric_dtype(df[col]):
            min_val, max_val = float(df[col].min()), float(df[col].max())
            user_input = st.slider(
                f"Filter {col}", min_val, max_val, (min_val, max_val)
            )
            df = df[df[col].between(*user_input)]
        elif is_datetime64_any_dtype(df[col]):
            user_input = st.date_input(f"Filter {col}", (df[col].min(), df[col].max()))
            if len(user_input) == 2:
                start_date, end_date = user_input
                df = df[df[col].between(start_date, end_date)]

    return df


# 예시 데이터프레임 생성
df = pd.DataFrame(
    {
        "Category": ["A", "B", "A", "C"],
        "Value": [10, 20, 30, 40],
        "Date": pd.date_range("2023-01-01", periods=4),
    }
)

# 필터링된 데이터프레임 표시
filtered_df = filter_dataframe(df)
st.dataframe(filtered_df)
