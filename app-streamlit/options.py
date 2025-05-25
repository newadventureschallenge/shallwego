import requests
import streamlit as st

from utils import api_endpoints


def side_options():
    if not st.session_state.get("token"):
        return

    options = ["openai-gpt-4.1-mini", "google-gemini-2.5-flash-preview-05-20", "anthropic-claude-3-5-haiku-latest"]

    # 세션에 없으면 첫 번째 옵션을 기본값으로 설정
    if "model" not in st.session_state:
        st.session_state.llm = options[0]

    # selectbox 표시 및 선택값 세션에 저장
    choice = st.selectbox("모델 선택", options, index=options.index(st.session_state.llm))
    st.session_state.llm = choice

    if st.button("전체 대화 삭제"):
        response = requests.delete(
            api_endpoints.RESET_API_URL,
            params={"user_id": st.session_state.get("user_id")}
        )

        if response.status_code == 200:
            st.success('전체 대화가 삭제되었습니다.')
        else:
            st.error(f'대화 삭제 실패: {response.status_code} - {response.text}')
