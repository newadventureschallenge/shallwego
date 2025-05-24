import functools

from langchain import requests


def handle_tool_exceptions(tool_name: str):
    """
    도구 실행 중 발생하는 예외를 처리하는 데코레이터입니다.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
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
    return {"Authorization": f"Bearer {access_token}"}
