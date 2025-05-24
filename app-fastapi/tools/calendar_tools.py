"""
카카오 API를 사용하여 캘린더 관련 작업을 수행하는 도구들입니다.
"""

from typing import Annotated

import requests
from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState

from agent.agent_state import State
from schemas.calendar_schemas import RequestCreateSubCalendar, RequestUpdateSubCalendar, RequestCalendarHoliday
from tools.tool_helpers import handle_tool_exceptions, get_access_token_header, get_rest_api_key_header, \
    get_service_app_admin_key_header
from utils import api_endpoints


@tool
@handle_tool_exceptions("캘린더 생성")
def create_calendar(
        state: Annotated[State, InjectedState],
        request: RequestCreateSubCalendar
):
    """
    카카오 캘린더 API를 사용하여 서브 캘린더를 생성합니다.
    """
    response = requests.post(
        url=api_endpoints.KAKAO_CREATE_CALENDAR_URL,
        headers=get_access_token_header(state.access_token),
        data=request.model_dump(),
        timeout=api_endpoints.API_TIMEOUT
    )

    return response


@tool
@handle_tool_exceptions("캘린더 목록 가져오기")
def get_calendar_list(
        state: Annotated[State, InjectedState]
):
    """
    카카오 캘린더 API를 사용하여 캘린더 목록을 가져옵니다.
    """
    response = requests.get(
        url=api_endpoints.KAKAO_GET_CALENDAR_URL,
        headers=get_access_token_header(state.access_token),
        timeout=api_endpoints.API_TIMEOUT
    )

    return response


@tool
@handle_tool_exceptions("캘린더 수정")
def update_calendar(
        state: Annotated[State, InjectedState],
        request: RequestUpdateSubCalendar
):
    """
    카카오 캘린더 API를 사용하여 서브 캘린더를 수정합니다.
    """
    response = requests.post(
        url=api_endpoints.KAKAO_UPDATE_CALENDAR_URL,
        headers=get_access_token_header(state.access_token),
        data=request.model_dump(),
        timeout=api_endpoints.API_TIMEOUT
    )

    return response


@tool
@handle_tool_exceptions("캘린더 삭제")
def delete_calendar(
        state: Annotated[State, InjectedState],
        request: RequestUpdateSubCalendar,
):
    """
    카카오 캘린더 API를 사용하여 서브 캘린더를 삭제합니다.
    """
    response = requests.delete(
        url=api_endpoints.KAKAO_DELETE_CALENDAR_URL,
        headers=get_access_token_header(state.access_token),
        params=request.model_dump(),
        timeout=api_endpoints.API_TIMEOUT
    )

    return response


@tool
@handle_tool_exceptions("공휴일 및 주요 기념일 조회하기")
def get_holidays(
        state: Annotated[State, InjectedState],
        request: RequestCalendarHoliday
):
    """
    카카오 캘린더 API를 사용하여 특정 연도의 공휴일 및 주요 기념일을 조회합니다.
    """
    response = requests.get(
        url=api_endpoints.KAKAO_GET_HOLIDAYS_URL,
        headers=get_service_app_admin_key_header(),
        params=request.model_dump(by_alias=True),
        timeout=api_endpoints.API_TIMEOUT
    )

    return response
