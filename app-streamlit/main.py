"""
Streamlit 메인 페이지
"""
import streamlit as st

# set_page_config 가 모든 streamlit 호출 중 제일 먼저 정의 되어야 함
st.set_page_config(
    page_title="갈까요-Shall We Go",
    page_icon="resources/mascot_icon.png",
)

from dotenv import load_dotenv

from page.chat import chat
from page.options import side_options
from page.social_login import manage_kakao_auth

load_dotenv()

st.title("갈까요-Shall We Go")

# 사이드바 로직 (로그인, 옵션 선택)
with st.sidebar:
    manage_kakao_auth()
    side_options()

# 메인 로직 (채팅 기능)
chat()
