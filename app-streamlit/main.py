"""
Streamlit 메인 페이지
"""
import streamlit as st

st.set_page_config(
    page_title="갈까요-Shall We Go",
    page_icon="resources/mascot_icon.png",
)

from dotenv import load_dotenv

from chat import chat
from social_login import manage_kakao_auth

load_dotenv()

st.title("갈까요-Shall We Go")

with st.sidebar:
    manage_kakao_auth()

chat()
