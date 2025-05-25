"""
도구 실행 중 발생하는 예외를 처리하는 데코레이터와 인증 헤더 생성 함수들
"""

import functools
import os

import requests

from utils.encryption import decrypt_message


def handle_tool_exceptions(tool_name: str):
    """
    도구 실행 중 발생하는 예외를 처리하는 데코레이터입니다.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"{tool_name} 실행")
            try:
                result = func(*args, **kwargs)
                if isinstance(result, requests.Response):
                    # status 코드가 200이 아닐 경우 예외 발생
                    if result.status_code != 200:
                        result.raise_for_status()

                    return result.json()

                return result

            except requests.exceptions.HTTPError as e:
                print(f"{tool_name} HTTP 오류 발생: {e.response.status_code} - {e.response.text}")

                return {
                    "error": f"{tool_name} HTTP 오류 발생: {e.response.status_code} - {e.response.text}"
                }
            except requests.exceptions.Timeout:
                print(f"{tool_name} 요청이 시간 초과되었습니다.")
                return {
                    "error": f"{tool_name} 요청이 시간 초과되었습니다. 다시 시도해주세요."
                }
            except Exception as e:
                print(f"{tool_name} 중 오류 발생: {str(e)}")
                return {
                    "error": f"{tool_name} 중 오류 발생: {str(e)}"
                }
        return wrapper
    return decorator


def get_access_token_header(access_token: str):
    """
    액세스 토큰을 사용하여 인증 헤더를 생성합니다.
    """
    return {"Authorization": f"Bearer {decrypt_message(access_token)}"}


def get_rest_api_key_header():
    """
    카카오 REST API 키를 사용하여 인증 헤더를 생성합니다.
    """
    rest_api_key = os.environ.get("KAKAO_APP_REST_API_KEY")
    return {"Authorization": f"KakaoAK {rest_api_key}"}


def get_service_app_admin_key_header():
    """
    카카오 서비스 앱 관리자 키를 사용하여 인증 헤더를 생성합니다.
    """
    service_app_admin_key = os.environ.get("KAKAO_APP_ADMIN_KEY")
    return {"Authorization": f"KakaoAK {service_app_admin_key}"}
