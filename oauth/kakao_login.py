"""
카카오 로그인 및 사용자 정보 가져오기
"""
import os
import time

import requests
import streamlit as st
from authlib.integrations.requests_client import OAuth2Session
from dotenv import load_dotenv
from streamlit_cookies_controller import CookieController

from utils import api_endpoints

load_dotenv()

cookie_controller = CookieController(key=os.getenv('STREAMLIT_COOKIE_SECRET_KEY'))

# 설정 로드
conf = st.secrets["auth"]["kakao"]

# OAuth2Session 객체 생성
oauth = OAuth2Session(
    client_id=conf["client_id"],
    client_secret=conf["client_secret"],
    scope="openid profile_nickname talk_calendar talk_calendar_task",
    redirect_uri=conf["redirect_uri"],
    token_endpoint_auth_method="client_secret_post"
)


def handle_oauth_callback():
    """OAuth 콜백을 처리하여 인가 코드를 액세스 토큰으로 교환"""
    params = st.query_params
    if params.get("code"):
        try:
            token = oauth.fetch_token(
                api_endpoints.KAKAO_API_TOKEN,
                code=params["code"],
            )
            st.session_state.token = token
            cookie_controller.set('token', token, max_age=3600)
            st.query_params.clear()
            st.rerun()
        except Exception as e:
            st.error(f"토큰 교환 중 오류 발생: {e}")


def fetch_user_info(access_token):
    """카카오 API를 사용하여 사용자 정보 가져오기"""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
    }

    return requests.get(
        url=api_endpoints.KAKAO_API_USER,
        headers=headers,
        timeout=api_endpoints.API_TIMEOUT
    )


def display_user_info(access_token):
    """사용자 정보를 가져와서 화면에 표시"""
    try:
        response = fetch_user_info(access_token)

        if response.status_code == 200:
            resp = response.json()
            nickname = resp["properties"]["nickname"]

            # 닉네임을 세션 상태에 저장
            st.session_state.user_nickname = nickname

            st.success(f"👋 **{nickname}**님, 안녕하세요!")

        else:
            st.error(f"카카오 API 호출 실패: {response.status_code}")
            st.error(f"응답 내용: {response.text}")

    except Exception as e:
        st.error(f"카카오 API 호출 오류: {e}")


def show_logout_button():
    """로그아웃 버튼을 표시하고 처리"""
    if st.button("로그아웃"):
        if "token" in st.session_state:
            del st.session_state.token
        st.rerun()


def show_login_button():
    """카카오 로그인 버튼을 표시"""
    auth_url, _ = oauth.create_authorization_url(api_endpoints.KAKAO_API_OAUTH)
    #st.markdown(f'<a href="{auth_url}" target="_self">카카오 로그인</a>', unsafe_allow_html=True)

    button_style = """
    <style>
    .kakao-login-button {
        display: inline-block; /* 버튼처럼 보이게 */
        padding: 10px 20px;
        background-color: #FEE500; /* 카카오 노란색 */
        color: #000000 !important; /* 검은색 글자, !important로 링크 기본색상 덮어쓰기 */
        text-align: center;
        text-decoration: none; /* 밑줄 제거 */
        font-size: 16px;
        font-weight: bold;
        border-radius: 5px; /* 모서리 둥글게 */
        border: 1px solid #FEE500;
        cursor: pointer; /* 마우스오버 시 커서 변경 */
        transition: background-color 0.2s; /* 부드러운 색상 변경 효과 */
    }
    .kakao-login-button:hover {
        background-color: #E6CF00; /* 호버 시 약간 어둡게 */
        text-decoration: none; /* 밑줄 제거 */
    }
    .kakao-login-button img { /* 아이콘 사용 시 */
        vertical-align: middle;
        margin-right: 8px;
    }
    </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)

    # 로그인 버튼 HTML (텍스트만)
    login_button_html = f'<a href="{auth_url}" target="_self" class="kakao-login-button">카카오 로그인</a>'

    st.markdown(login_button_html, unsafe_allow_html=True)


def ensure_valid_token():
    """세션에 저장된 토큰이 만료되었으면 refresh_token으로 갱신"""
    token = st.session_state.token
    # expires_at: Unix timestamp 로 저장되어 있다고 가정
    if time.time() > token.get("expires_at", 0):
        # refresh_token 으로 새 토큰 요청
        new_token = oauth.refresh_token(
            api_endpoints.KAKAO_API_TOKEN,
            refresh_token=token["refresh_token"],
        )
        # 세션과 쿠키에 업데이트
        st.session_state.token = new_token
        cookie_controller.set("token", new_token, max_age=3600)


def manage_kakao_auth():
    """카카오 인증 흐름 전체 관리"""
    # OAuth 콜백 처리
    handle_oauth_callback()

    if "token" not in st.session_state:
        tok = cookie_controller.get("token")
        if tok:
            st.session_state.token = tok

    # 로그인 상태에 따라 다른 UI 표시
    if st.session_state.get("token"):
        display_user_info(st.session_state.token.get("access_token"))
        show_logout_button()
    else:
        show_login_button()
