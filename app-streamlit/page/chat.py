"""
에이전트 채팅
"""
import time

import orjson
import streamlit as st
from websocket import create_connection, WebSocketConnectionClosedException

from page.social_login import ensure_valid_token
from schemas.chat_schemas import ChatRequest
from utils import api_endpoints
from utils.encryption import encrypt_message

# 챗봇 아이콘 설정
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

    nickname = str(st.session_state.get("nickname"))
    access_token = str(st.session_state.token.get("access_token"))
    user_id = str(st.session_state.get("user_id"))

    # 채팅 상태 초기화 및 최초 인사말 출력
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "assistant",
            "content": "🌏 안녕하세요! 당신의 여행 에이전트, '갈까요' 입니다. 무엇을 도와드릴까요?"
        })

    # 채팅 히스토리 전체 출력
    for message in st.session_state.messages:
        avatar = avatar_icon[message["role"]]
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # 사용자 대화 입력
    if prompt := st.chat_input("대화를 입력해주세요."):
        # 토큰 만료 확인 및 재발급
        ensure_valid_token()

        # 사용자 메시지 출력 및 히스토리 추가
        with st.chat_message("user", avatar=avatar_icon["user"]):
            st.markdown(prompt)
            
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # 챗봇 메시지 출력 및 히스토리 추가
        with st.chat_message("assistant", avatar=avatar_icon["assistant"]):
            assistant_placeholder = st.empty()
    
        st.session_state.messages.append({"role": "assistant", "content": ""})
        
        assistant_index = len(st.session_state.messages) - 1

        # 웹 소켓 연결
        ws = create_connection(api_endpoints.CHAT_API_URL)
        
        # 요청 Schema
        req = ChatRequest(
            message=prompt,
            nickname=nickname,
            user_id=user_id,
            access_token=encrypt_message(access_token),
            model_id=st.session_state.llm
        ).model_dump()
        
        full_response = ""

        try:
            # request 전달
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

                    parts = message.get("messages", [])

                    # Claude의 경우 Chunk가 바로 넘어오지 않고 []에 담겨 오기 때문에 추가적으로 설정한 로직
                    if isinstance(parts, list):
                        for chunk in parts:
                            # 안전하게 text 키를 꺼내서 더하기
                            full_response += chunk.get("text", "")
                    else:
                        full_response += str(parts)

                    st.session_state.messages[assistant_index]['content'] = full_response

                    assistant_placeholder.markdown(full_response, unsafe_allow_html=True)

                    # UI 업데이트를 위한 짧은 대기
                    time.sleep(0.01)

                except WebSocketConnectionClosedException:
                    break
        finally:
            ws.close()

        # 메시지의 가장 마지막에 chunk를 모두 모은 full_response 로 챗봇 메시지 완성
        st.session_state.messages[assistant_index]['content'] = full_response
