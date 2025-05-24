"""
카카오 API를 사용하여 로컬 작업을 수행하는 Tool Node 입니다.
"""

import requests
from langchain_core.tools import tool

from schemas.local_schemas import RequestLocalSearchCategory, RequestLocalSearchKeyword
from tools.tool_helpers import handle_tool_exceptions, get_rest_api_key_header
from utils import api_endpoints


@tool
@handle_tool_exceptions("키워드로 장소 검색하기")
def search_places_by_keyword(
        request: RequestLocalSearchKeyword
):
    """
    카카오 로컬 API를 사용하여 키워드로 장소를 검색합니다.
    """
    response = requests.get(
        url=api_endpoints.KAKAO_LOCAL_SEARCH_KEYWORD_URL,
        headers=get_rest_api_key_header(),
        params=request.model_dump(),
        timeout=api_endpoints.API_TIMEOUT
    )

    return response


@tool
@handle_tool_exceptions("카테고리로 장소 검색하기")
def search_places_by_category(
        request: RequestLocalSearchCategory
):
    """
    카카오 로컬 API를 사용하여 카테고리로 장소를 검색합니다.
    """
    response = requests.get(
        url=api_endpoints.KAKAO_LOCAL_SEARCH_CATEGORIES_URL,
        headers=get_rest_api_key_header(),
        params=request.model_dump(),
        timeout=api_endpoints.API_TIMEOUT
    )

    return response
