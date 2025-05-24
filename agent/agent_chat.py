"""
에이전트 채팅
"""
import streamlit as st
from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableConfig

from agent.agent_graph import graph


def chat():
    """
    에이전트 채팅
    """
    # 만약 발급받은 토큰이 없다면 대화창을 출력하지 않음
    if not st.session_state.get("token"):
        st.warning("로그인 후 사용 가능합니다.")
        return

    access_token = st.session_state.token.get("access_token")

    # 채팅 상태 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "assistant",
            "content": "안녕하세요! 당신의 여행 에이전트, '갈까요' 입니다. 무엇을 도와드릴까요?"
        })

    if "consent_pending" not in st.session_state:  # 동의 대기 중인지 여부
        st.session_state.consent_pending = False

    if "pending_ai_message_with_tool_calls" not in st.session_state:  # 도구 사용을 제안한 AI 메시지 임시 저장
        st.session_state.pending_ai_message_with_tool_calls = None

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
            response = st.write_stream(response_generator(access_token, st.session_state.messages))

        # 추가된 버튼 예시
        if st.button("이 단계 진행하기", key=f"confirm_{len(st.session_state.messages)}"):
            # 버튼 클릭 시 실행할 로직
            st.write("버튼이 눌렸습니다! 다음 작업을 수행합니다.")
            # 예: 특정 도구 호출, 백엔드 API 요청 등

        st.session_state.messages.append({"role": "assistant", "content": response})


def response_generator(access_token, messages):
    """
    청크 단위 스트리밍을 위한 async 제너레이터 반환
    """
    async def _stream():
        """
        스트리밍 제너레이터
        """
        config = RunnableConfig(
            recursion_limit=10,  # 최대 10개의 노드까지 방문. 그 이상은 RecursionError 발생
            configurable={"thread_id": "1"},  # 스레드 ID 설정
        )

        async for chunk, _ in graph.astream(
                input={"access_token": access_token, "messages": messages},
                stream_mode="messages",
                config=config,
                # interrupt_before=["tools"]
        ):
            # chunk.content 가 비어있지 않으면 그대로 내보냄
            if isinstance(chunk, ToolMessage):
                continue

            content = getattr(chunk, "content", None)
            if content:
                yield content

        # if graph.get_state(config).next[0] == "tools":
        #     # 도구 호출이 필요한 경우
        #     yield "도구 호출이 필요합니다. 도구를 사용하여 검색을 진행합니다."

    # async 제너레이터 객체 자체를 반환
    return _stream()
