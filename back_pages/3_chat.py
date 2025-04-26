import streamlit as st

# 세션 상태 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 채팅 입력 받기
if prompt := st.chat_input("찾고 싶은 장소를 입력해 주세요."):
    response = (
        f"{prompt}에 대한 답변입니다."  # 여기에 실제 답변 로직을 추가할 수 있습니다.
    )
    st.session_state.chat_history.append((prompt, response))

# CSS 스타일 정의
st.markdown(
    """
    <style>
    .user-message {
        text-align: right;
        background-color: #f7f8fa;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        color: black;
    }
    .copilot-message {
        text-align: left;
        background-color: #FAF1CF;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        color: black;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 채팅 기록 출력
for question, answer in st.session_state.chat_history:
    st.markdown(
        f"<div class='user-message'>{question}</div>",
        unsafe_allow_html=True,
    )
    st.chat_message("assistant").write(answer)
