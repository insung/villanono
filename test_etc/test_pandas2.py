import pandas as pd

# 예제 DataFrame 생성
data = {
    "시": [
        "서울특별시",
        "서울특별시",
        "서울특별시",
        "서울특별시",
        "서울특별시",
        "서울특별시",
    ],
    "군구": ["강남구", "강남구", "강남구", "강남구", "용산구", "용산구"],
    "동": ["개포동", "논현동", "대치동", "도곡동", "효창동", "후암동"],
}
df = pd.DataFrame(data)

# 딕셔너리 생성
result = {}
for 시, 군구, 동 in zip(df["시"], df["군구"], df["동"]):
    if 시 not in result:
        result[시] = {}
    if 군구 not in result[시]:
        result[시][군구] = []
    result[시][군구].append(동)

print(result)
