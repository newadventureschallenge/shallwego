"""
에이전트 채팅
"""
import time

import orjson
import streamlit as st
from websocket import create_connection, WebSocketConnectionClosedException

from schemas.chat_schemas import ChatRequest
from social_login import ensure_valid_token
from utils import api_endpoints

avatar_icon = {
    'user': 'resources/traveler_icon.png',
    'assistant': 'resources/mascot_icon.png'
}

def chat():
    """
    에이전트 채팅
    """
    # 만약 발급받은 토큰이 없다면 대화창을 출력하지 않음
    if not st.session_state.get("token"):
        st.warning("로그인 후 사용 가능합니다.")
        st.image('resources/front_image.png')
        return

    access_token = str(st.session_state.token.get("access_token"))
    user_id = str(st.session_state.get("user_id"))

    # 채팅 상태 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "assistant",
            "content": "🌏 안녕하세요! 당신의 여행 에이전트, '갈까요' 입니다. 무엇을 도와드릴까요?"
        })

    if "consent_pending" not in st.session_state:  # 동의 대기 중인지 여부
        st.session_state.consent_pending = False

    if "pending_ai_message_with_tool_calls" not in st.session_state:  # 도구 사용을 제안한 AI 메시지 임시 저장
        st.session_state.pending_ai_message_with_tool_calls = None

    # 채팅 히스토리 출력
    for message in st.session_state.messages:
        avatar = avatar_icon[message["role"]]
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # 대화 입력
    if prompt := st.chat_input("대화를 입력해주세요."):
        # 토큰 만료 확인
        ensure_valid_token()

        # 사용자 메시지 출력
        with st.chat_message("user", avatar=avatar_icon["user"]):
            st.markdown(prompt)

        # 사용자 메시지 채팅 히스토리 추가
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("assistant", avatar=avatar_icon["assistant"]):
            assistant_placeholder = st.empty()

        st.session_state.messages.append({"role": "assistant", "content": ""})
        assistant_index = len(st.session_state.messages) - 1

        ws = create_connection(api_endpoints.CHAT_API_URL)
        req = ChatRequest(message=prompt, user_id=user_id, access_token=access_token).model_dump()
        full_response = ""

        try:
            ws.send(orjson.dumps(req))

            while True:
                try:
                    raw = ws.recv()
                    if not raw:
                        continue

                    try:
                        message = orjson.loads(raw)
                    except orjson.JSONDecodeError:
                        continue

                    full_response += message['messages']
                    st.session_state.messages[assistant_index]['content'] = full_response
                    assistant_placeholder.markdown(full_response, unsafe_allow_html=True)
                    time.sleep(0.01) # UI 업데이트를 위한 짧은 대기

                except WebSocketConnectionClosedException:
                    break
        finally:
            ws.close()

        st.session_state.messages[assistant_index]['content'] = full_response
