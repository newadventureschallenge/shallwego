import json
from typing import Annotated

import requests
from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState

from agent.agent_state import State
from schemas.event_schemas import RequestCreateEvent, RequestGetEvents, RequestDeleteEvent, RequestUpdateEvent
from tools.tool_helpers import get_access_token_header, handle_tool_exceptions
from utils import api_endpoints


@tool
@handle_tool_exceptions("일반 일정 생성")
def create_event(
        state: Annotated[State, InjectedState],
        request: RequestCreateEvent
):
    """
    카카오 캘린더 API를 사용하여 일반 일정을 생성합니다.
    """
    # 1) None 필드는 빼고 dict 생성
    payload_dict = request.model_dump(exclude_none=True)

    # 2) event만 JSON 문자열로 변환
    event_str = json.dumps(payload_dict["event"], ensure_ascii=False)

    # 3) calendar_id와 event 두 개로 payload 구성
    form_data = {
        "calendar_id": payload_dict["calendar_id"],
        "event": event_str
    }

    response = requests.post(
        url=api_endpoints.KAKAO_CREATE_EVENT_URL,
        headers=get_access_token_header(state.access_token),
        data=form_data,
        timeout=api_endpoints.API_TIMEOUT
    )

    return response.json()


@tool
@handle_tool_exceptions("일반 일정 목록 가져오기")
def get_event_list(
        state: Annotated[State, InjectedState],
        request: RequestGetEvents
):
    """
    카카오 캘린더 API를 사용하여 일반 일정 목록을 가져옵니다.
    """
    response = requests.get(
        url=api_endpoints.KAKAO_GET_EVENTS_URL,
        headers=get_access_token_header(state.access_token),
        params=request.model_dump(),
        timeout=api_endpoints.API_TIMEOUT
    )

    return response.json()


@tool
@handle_tool_exceptions("일반 일정 상세 조회")
def get_event_detail(
        state: Annotated[State, InjectedState],
        request: RequestGetEvents,
):
    """
    카카오 캘린더 API를 사용하여 일반 일정의 상세 정보를 조회합니다.
    """
    response = requests.get(
        url=api_endpoints.KAKAO_GET_EVENT_URL,
        headers=get_access_token_header(state.access_token),
        params=request.model_dump(),
        timeout=api_endpoints.API_TIMEOUT
    )

    return response.json()


@tool
@handle_tool_exceptions("일반 일정 수정")
def update_event(
        state: Annotated[State, InjectedState],
        request: RequestUpdateEvent
):
    """
    카카오 캘린더 API를 사용하여 일반 일정을 수정합니다.
    """
    # 1) None 필드는 빼고 dict 생성
    payload_dict = request.model_dump(exclude_none=True)

    # 2) event만 JSON 문자열로 변환
    event_str = json.dumps(payload_dict["event"], ensure_ascii=False)

    # 3) calendar_id와 event 두 개로 payload 구성
    form_data = {
        "calendar_id": payload_dict["calendar_id"],
        "event": event_str
    }

    response = requests.post(
        url=api_endpoints.KAKAO_UPDATE_EVENT_URL,
        headers=get_access_token_header(state.access_token),
        data=form_data,
        timeout=api_endpoints.API_TIMEOUT
    )

    return response.json()


@tool
@handle_tool_exceptions("일반 일정 삭제")
def delete_event(
        state: Annotated[State, InjectedState],
        request: RequestDeleteEvent
):
    """
    카카오 캘린더 API를 사용하여 일반 일정을 삭제합니다.
    """
    response = requests.delete(
        url=api_endpoints.KAKAO_DELETE_EVENT_URL,
        headers=get_access_token_header(state.access_token),
        params=request.model_dump(),
        timeout=api_endpoints.API_TIMEOUT
    )

    return response.json()
