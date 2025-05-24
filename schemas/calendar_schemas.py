"""
사용자 캘린더 스키마 정의
"""
from typing import Optional

from pydantic import BaseModel, Field

from utils.enums import ColorEnum


class RequestCreateSubCalendar(BaseModel):
    """생성하기: 서브 캘린더"""
    name: str = Field(None, max_length=50, description="캘린더 이름 (최대 50자)")
    color: Optional[ColorEnum] = Field(None, description="캘린더 색상, Color 중 하나(기본값: BLUE)")
    reminder: Optional[int] = Field(None, description="종일이 아닌 일정의 기본 알림 설정, 5분 간격으로 설정 가능하며 null 전달 시 값 초기화")
    reminder_all_day: Optional[int] = Field(None, description="종일 일정의 기본 알림 설정, 5분 간격으로 설정 가능하며 null 전달 시 값 초기화")


class RequestUpdateSubCalendar(BaseModel):
    """수정하기: 서브 캘린더"""
    calendar_id: str = Field(..., description="서브 캘린더 ID")
    name: Optional[str] = Field(None, max_length=50, description="캘린더 이름 (최대 50자)")
    color: Optional[ColorEnum] = Field(None, description="캘린더 색상, Color 중 하나(기본값: BLUE)")
    reminder: Optional[int] = Field(None, description="종일이 아닌 일정의 기본 알림 설정, 5분 간격으로 설정 가능하며 null 전달 시 값 초기화")
    reminder_all_day: Optional[int] = Field(None, description="종일 일정의 기본 알림 설정, 5분 간격으로 설정 가능하며 null 전달 시 값 초기화")
