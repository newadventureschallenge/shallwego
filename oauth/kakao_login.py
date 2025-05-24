"""
카카오 로그인 및 사용자 정보 가져오기
"""

import os

import requests
import streamlit as st

from authlib.integrations.requests_client import OAuth2Session

# 설정 로드
conf = st.secrets["auth"]["kakao"]

# OAuth2Session 객체 생성
oauth = OAuth2Session(
    client_id=conf["client_id"],
    client_secret=conf["client_secret"],
    scope="openid profile_nickname talk_calendar",
    redirect_uri=conf["redirect_uri"],
    token_endpoint_auth_method="client_secret_post"
)


def handle_oauth_callback():
    """OAuth 콜백을 처리하여 인가 코드를 토큰으로 교환"""
    params = st.query_params
    if params.get("code"):
        try:
            token = oauth.fetch_token(
                os.getenv("KAKAO_API_TOKEN"),
                code=params["code"],
            )
            st.session_state.token = token
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

    return requests.get(os.getenv("KAKAO_API_USER"), headers=headers)


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

            url = "https://kapi.kakao.com/v2/api/calendar/calendars"
            response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
            if response.status_code == 200:
                calendars = response.json()
                st.write(calendars)
            else:
                st.error(f"캘린더 API 호출 실패: {response.status_code}")
                st.error(f"응답 내용: {response.text}")

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
    auth_url, _ = oauth.create_authorization_url(os.getenv("KAKAO_API_OAUTH"))
    st.markdown(f'<a href="{auth_url}" target="_self">카카오 로그인</a>', unsafe_allow_html=True)


def manage_kakao_auth():
    """카카오 인증 흐름 전체 관리"""
    # OAuth 콜백 처리
    handle_oauth_callback()

    # 로그인 상태에 따라 다른 UI 표시
    if st.session_state.get("token"):
        display_user_info(st.session_state.token.get("access_token"))
        show_logout_button()
    else:
        show_login_button()
