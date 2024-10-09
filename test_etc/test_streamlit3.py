import streamlit as st

# 옵션과 실제 값을 정의
options = ["Option 1", "Option 2", "Option 3"]
values = [10, 20, 30]


# 옵션을 실제 값으로 매핑하는 함수
def format_func(option):
    return f"{option} (Value: {values[options.index(option)]})"


# selectbox 생성
selected_option = st.selectbox("옵션을 선택하세요:", options, format_func=format_func)

# 선택한 옵션의 실제 값 가져오기
selected_value = values[options.index(selected_option)]
st.write("선택한 옵션의 실제 값:", selected_value)
