"""
에이전트 채팅
"""
import streamlit as st

from agent_graph import graph


def chat():
    """
    에이전트 채팅
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

        with st.chat_message("assistant"):
            response = st.write_stream(response_generator(st.session_state.messages))

        st.session_state.messages.append({"role": "assistant", "content": response})


def response_generator(messages):
    """
    청크 단위 스트리밍을 위한 async 제너레이터 반환
    """
    async def _stream():
        """
        스트리밍 제너레이터
        """
        async for chunk, _ in graph.astream(input={"messages": messages}, stream_mode="messages"):
            # chunk.content 가 비어있지 않으면 그대로 내보냄
            content = getattr(chunk, "content", None)
            if content:
                yield content

    # async 제너레이터 객체 자체를 반환
    return _stream()
