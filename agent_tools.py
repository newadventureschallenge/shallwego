import os

import requests
from dotenv import load_dotenv

from langchain_core.tools import tool

load_dotenv()

@tool
def daum_web_search(query: str, sort: str = "accuracy", page: int = 1, size: int = 30):
    """Kakao API를 사용하여 Daum 웹 검색을 실행합니다."""
    rest_api_key = os.environ.get("KAKAO_APP_REST_API_KEY")
    if not rest_api_key:
        return "Kakao REST API 키가 설정되지 않았습니다. 환경 변수 KAKAO_REST_API_KEY를 설정해주세요."

    url = "https://dapi.kakao.com/v2/search/web"
    headers = {"Authorization": f"KakaoAK {rest_api_key}"}
    params = {"query": query, "sort": sort, "page": page, "size": size}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 처리

        # 콘솔 출력으로 json 결과 확인
        print(f"Daum Web Search API 검색어: {query}")
        print(response.json())

        return response.json()
    except requests.exceptions.HTTPError as e:
        return f"HTTP 오류 발생: {e.response.status_code} - {e.response.text}"
    except requests.exceptions.Timeout as e:
        return "요청이 시간 초과되었습니다. 다시 시도해주세요."
    except Exception as e:
        return f"오류 발생: {str(e)}"


tools = [daum_web_search]
