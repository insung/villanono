import pandas as pd
from pandas.api.types import CategoricalDtype

# 예제 DataFrame 생성
df = pd.DataFrame(
    {
        "도시": [
            "서울특별시",
            "부산광역시",
            "대구광역시",
            "인천광역시",
            "광주광역시",
            "대전광역시",
            "울산광역시",
        ]
    }
)

# 사용자 정의 정렬 순서 정의
custom_order = ["서울특별시", "부산광역시"]
all_categories = custom_order + sorted(set(df["도시"]) - set(custom_order))
cat_type = CategoricalDtype(categories=all_categories, ordered=True)

# '도시' 열을 Categorical 타입으로 변환
df["도시"] = df["도시"].astype(cat_type)

# 사용자 정의 순서로 정렬
df_sorted = df.sort_values(by="도시")

print(df_sorted)

"""
      도시
0  서울특별시
1  부산광역시
4  광주광역시
2  대구광역시
5  대전광역시
6  울산광역시
3  인천광역시
"""
