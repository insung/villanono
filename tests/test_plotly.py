import pandas as pd
import seaborn as sns

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

selected = df2[["계약년월", "계약건수"]]

# fig = px.line(selected, x="계약년월", y="계약건수")
# fig.show()

sns.barplot(data=selected, x="계약년월", y="계약건수")
