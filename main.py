"""
Streamlit 메인 페이지
"""
import streamlit as st

from dotenv import load_dotenv

from agent_chat import chat
from kakao_login import manage_kakao_auth

load_dotenv()

st.title("갈까요-Shall we go")

with st.sidebar:
    manage_kakao_auth()

chat()
