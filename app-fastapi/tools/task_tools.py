"""
카카오 API를 사용하여 할 일 관련 작업을 수행하는 Tool Node 입니다.
"""

import json
from typing import Annotated

import requests
from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState

from agent.agent_state import State
from schemas.task_schemas import RequestDeleteTask, RequestCompleteTask, RequestUpdateTask, RequestTaskRecords, \
    RequestCreateTask, RequestGetTasks
from tools.tool_helpers import handle_tool_exceptions, get_access_token_header
from utils import api_endpoints


@tool
@handle_tool_exceptions("할 일 생성하기")
def create_task(
        status: Annotated[State, InjectedState],
        request: RequestCreateTask
):
    """
    카카오 API를 사용하여 할 일을 생성합니다.
    """
    # 1) Pydantic 모델에서 dict 형태로 꺼내기
    payload = request.model_dump(exclude_none=True)
    task_obj = payload["task"]

    # 2) task_obj를 JSON 문자열로 직렬화
    task_str = json.dumps(task_obj, ensure_ascii=False)

    response = requests.post(
        url=api_endpoints.KAKAO_CREATE_TASK_URL,
        headers=get_access_token_header(access_token=status.access_token),
        data={"task": task_str},
        timeout=api_endpoints.API_TIMEOUT
    )

    return response


@tool
@handle_tool_exceptions("할 일 목록 가져오기")
def get_tasks(
        status: Annotated[State, InjectedState],
        request: RequestGetTasks
):
    """
    카카오 API를 사용하여 할 일 목록을 조회합니다.
    """
    response = requests.get(
        url=api_endpoints.KAKAO_GET_TASKS_URL,
        headers=get_access_token_header(access_token=status.access_token),
        params=request.model_dump(exclude_none=True, by_alias=True),
        timeout=api_endpoints.API_TIMEOUT
    )

    return response


@tool
@handle_tool_exceptions("할 일 도전 기록 보기")
def records_task(
        status: Annotated[State, InjectedState],
        request: RequestTaskRecords
):
    """
    카카오 API를 사용하여 할 일 도전 기록을 조회합니다.
    """
    response = requests.get(
        url=api_endpoints.KAKAO_RECORDS_TASK_URL,
        headers=get_access_token_header(access_token=status.access_token),
        params=request.model_dump(exclude_none=True, by_alias=True),
        timeout=api_endpoints.API_TIMEOUT
    )

    return response


@tool
@handle_tool_exceptions("할 일 수정하기")
def update_task(
        status: Annotated[State, InjectedState],
        request: RequestUpdateTask
):
    """
    카카오 API를 사용하여 할 일을 수정합니다.
    """
    # 1) Pydantic 모델에서 dict 형태로 꺼내기
    payload = request.model_dump(exclude_none=True)
    task_obj = payload["task"]

    # 2) task_obj를 JSON 문자열로 직렬화
    task_str = json.dumps(task_obj, ensure_ascii=False)

    response = requests.post(
        url=api_endpoints.KAKAO_UPDATE_TASK_URL,
        headers=get_access_token_header(access_token=status.access_token),
        data={"task_id": request.task_id, "task": task_str},
        timeout=api_endpoints.API_TIMEOUT
    )

    return response


@tool
@handle_tool_exceptions("할 일 완료 여부 설정하기")
def complete_task(
        status: Annotated[State, InjectedState],
        request: RequestCompleteTask
):
    """
    카카오 API를 사용하여 할 일 완료 여부를 설정합니다.
    """
    response = requests.post(
        url=api_endpoints.KAKAO_COMPLETE_TASK_URL,
        headers=get_access_token_header(access_token=status.access_token),
        data=request.model_dump(exclude_none=True),
        timeout=api_endpoints.API_TIMEOUT
    )

    return response


@tool
@handle_tool_exceptions("할 일 삭제하기")
def delete_task(
        status: Annotated[State, InjectedState],
        request: RequestDeleteTask
):
    """
    카카오 API를 사용하여 할 일을 삭제합니다.
    """
    response = requests.delete(
        url=api_endpoints.KAKAO_DELETE_TASK_URL,
        headers=get_access_token_header(access_token=status.access_token),
        params=request.model_dump(exclude_none=True),
        timeout=api_endpoints.API_TIMEOUT
    )

    return response
