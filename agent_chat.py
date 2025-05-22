"""
에이전트 채팅
"""

import streamlit as st

def chat():
    """
    에이전트 채팅 (현재 Dummy Response)
    """
    # 만약 발급받은 토큰이 없다면 대화창을 출력하지 않음
    if not st.session_state.get("token"):
        st.warning("로그인 후 사용 가능합니다.")
        return

    # 채팅 상태 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 채팅 히스토리 출력
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 대화 입력
    if prompt := st.chat_input("대화를 입력해주세요."):
        # 사용자 메시지 출력
        st.chat_message("user").markdown(prompt)

        # 사용자 메시지 채팅 히스토리 추가
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Dummy Response 추가
        response = f"Echo: {prompt}"

        # Assistant 메시지 출력
        with st.chat_message("assistant"):
            st.markdown(response)

        # Assistant 메시지 채팅 히스토리 추가
        st.session_state.messages.append({"role": "assistant", "content": response})
