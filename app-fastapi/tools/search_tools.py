"""
카카오 API를 사용하여 Daum 검색을 수행하는 Tool Node 입니다.
"""

import requests
from langchain_core.tools import tool

from schemas.search_schemas import RequestWebSearch
from tools.tool_helpers import handle_tool_exceptions, get_rest_api_key_header
from utils import api_endpoints


@tool
@handle_tool_exceptions("웹 문서 검색하기")
def daum_web_search(
        request: RequestWebSearch
):
    """Kakao API를 사용하여 Daum 웹 검색을 실행합니다."""
    headers = get_rest_api_key_header()
    params = request.model_dump()

    response = requests.get(
        url=api_endpoints.KAKAO_DAUM_SEARCH_URL,
        headers=headers,
        params=params,
        timeout=api_endpoints.API_TIMEOUT
    )

    return response
