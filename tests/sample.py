import matplotlib.pyplot as plt

from util import read_original_file

df2023 = read_original_file("2023전월세.csv")
df2024 = read_original_file("2024전월세.csv")

dfplot2023 = df2023.query("전월세구분 == '전세' & 계약년월 == 202301")[
    ["계약년월", "보증금(만원)"]
].groupby("계약년월", as_index=False)

plt.figure()
dfplot2023.plot()
