import os

import requests
from langchain_core.tools import tool

from schemas.search_schemas import RequestWebSearch
from tools.tool_helpers import handle_tool_exceptions
from utils import api_endpoints


@tool
@handle_tool_exceptions("웹 문서 검색하기")
def daum_web_search(
        request: RequestWebSearch
):
    """Kakao API를 사용하여 Daum 웹 검색을 실행합니다."""
    rest_api_key = os.environ.get("KAKAO_APP_REST_API_KEY")
    if not rest_api_key:
        return "Kakao REST API 키가 설정되지 않았습니다. 환경 변수 KAKAO_REST_API_KEY를 설정해주세요."

    headers = {"Authorization": f"KakaoAK {rest_api_key}"}
    params = request.model_dump()

    response = requests.get(
        api_endpoints.KAKAO_DAUM_SEARCH_URL,
        headers=headers,
        params=params,
        timeout=api_endpoints.API_TIMEOUT
    )
    response.raise_for_status()

    return response.json()
