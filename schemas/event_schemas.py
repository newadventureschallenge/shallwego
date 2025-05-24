from typing import Optional

from pydantic import BaseModel, Field

from schemas.common_schemas import Time, Location
from utils.enums import ColorEnum


class EventCreate(BaseModel):
    """일정 생성 시 필요한 정보"""
    title: str = Field(..., max_length=50, description="일정 제목 (최대 50자)")
    time: Time = Field(..., description="일정 시간")
    rrule: Optional[str] = Field(None, description='''
    일정의 반복 주기, UTC*, RFC5545의 RRULE 형식(예: FREQ=DAILY;UNTIL=20211208T155959Z)
    주의: 해당 파라미터 포함 시 반복 일정 생성''')
    description: Optional[str] = Field(None, max_length=5000, description="일정 설명 (최대 5000자)")
    location: Optional[Location] = Field(None, description="일정 장소")
    reminders: Optional[int] = Field(None, description='''
    미리 알림 설정(단위: 분), 5분 간격으로 최대 2개 설정 가능
    종일 일정 범위: -1440(일정 당일이 끝나기 전) < 알림값 ≤ 43200(일정 시작 30일 전), (기본값: 해당 캘린더의 reminder 값)
    종일 일정이 아닌 일정 범위: 0(일정 시작 시각) < 알림값 ≤ 43200(일정 시작 30일 전), (기본값: 해당 캘린더의 reminder_all_day 값)''')
    color: Optional[ColorEnum] = Field(None, description="일정 색상, Color 중 하나 (기본값: 해당 캘린더의 color 값)")


class EventUpdate(BaseModel):
    """일정 수정 시 필요한 정보"""
    title: Optional[str] = Field(None, max_length=50, description="일정 제목 (최대 50자)")
    time: Optional[Time] = Field(None, description="일정 시간(기본값: 기존 유지)")
    rrule: Optional[str] = Field(None, description='''
    일정의 반복 주기, UTC*, RFC5545의 RRULE 형식(예: FREQ=DAILY;UNTIL=20211208T155959Z, 기본값: 기존 유지)''')
    description: Optional[str] = Field(None, max_length=5000, description="일정 설명 (최대 5000자, 기본값: 기존 유지)")
    location: Optional[Location] = Field(None, description="일정 장소(기본값: 기존 유지)")
    reminders: Optional[int] = Field(None, description='''
    미리 알림 설정(단위: 분), 5분 간격으로 최대 2개 설정 가능
    종일 일정 범위: -1440(일정 당일이 끝나기 전) < 알림값 ≤ 43200(일정 시작 30일 전), (기본값: 기존 유지)
    종일 일정이 아닌 일정 범위: 0(일정 시작 시각) < 알림값 ≤ 43200(일정 시작 30일 전), (기본값: 기존 유지)''')
    color: Optional[ColorEnum] = Field(None, description="일정 색상, Color 중 하나 (기본값: 기존 유지)")


class RequestCreateEvent(BaseModel):
    """일정 생성하기"""
    calendar_id: str = Field(..., description="일정을 생성할 캘린더 ID(기본값: primary)")
    event: EventCreate = Field(..., description="생성할 일정 정보")


class RequestGetEvents(BaseModel):
    """일정 조회하기"""
    calendar_id: Optional[str] = Field(..., description="일정을 조회할 캘린더 ID(기본값: 전체 캘린더 조회)")
    preset: Optional[str] = Field(None, description='''
    미리 정의된 일정 조회 기간, 아래 중 하나
    TODAY: 조회 당일
    THIS_WEEK: 일요일로 시작하는 조회일이 포함된 한 주
    THIS_MONTH: 1일로 시작하는 조회일이 포함된 한 달

    주의: from과 to가 포함되지 않은 경우 필수
    주의: next_page_token가 포함된 경우 무시됨''')
    time_zone: Optional[str] = Field("Asia/Seoul", description="기한 일자의 타임존, UTC*, RFC5545의 TZID 형식(기본값: Asia/Seoul)")
    from_: Optional[str] = Field(None, alias="from", description='''
    일정을 조회할 기간의 시작 시각, UTC*, RFC5545의 DATE-TIME 형식(예: 2022-05-17T12:00:00Z)
    주의: preset 또는 next_page_token가 포함된 경우 무시됨''')
    to: Optional[str] = Field(None, description='''
    일정을 조회할 기간의 종료 시각, from 이후 31일 이내의 값, UTC*, RFC5545의 DATE-TIME 형식(예: 2022-06-17T12:00:00Z)
    주의: preset 또는 next_page_token가 포함된 경우 무시됨''')
    limit: Optional[int] = Field(100, ge=1, le=100, description='''
    응답으로 받을 최대 일정 수(최대: 1000, 기본값: 100)
    주의: preset 또는 next_page_token가 포함된 경우 무시됨''')
    next_page_token: Optional[str] = Field(None, description='''
    다음 페이지 조회를 위한 from, to, limit 값이 포함된 조회 조건 토큰, 응답으로 받은 after_url에서 확인 가능''')

    class Config:
        validate_by_name = True
        allow_population_by_alias = True


class RequestGetEvent(BaseModel):
    """상세 조회하기"""
    event_id: str = Field(..., description="일정 ID")


class RequestUpdateEvent(BaseModel):
    """일정 수정하기"""
    event_id: str = Field(..., description="일정 ID")
    calendar_id: Optional[str] = Field(None, description='''
    캘린더 ID(기본값: 기존 유지)

    주의: event를 포함하지 않은 경우 필수
    중요: 기본 캘린더 또는 서비스에서 직접 생성한 서브 캘린더의 ID만 지정 가능''')
    recur_update_type: Optional[str] = Field(None, description='''
    반복 일정의 수정 범위, 아래 중 하나
    ALL: 전체 일정
    THIS: 이 일정만
    THIS_AND_FOLLOWING: 이 일정과 이후 모든 일정

    주의: 반복 일정인 경우 필수''')
    event: Optional[EventUpdate] = Field(None, description="수정할 일정 정보. 주의: calendar_id가 포함된 경우 필수")

class RequestDeleteEvent(BaseModel):
    """일정 삭제하기"""
    event_id: str = Field(..., description="일정 ID")
    recur_update_type: Optional[str] = Field(None, description='''
    반복 일정의 수정 범위
    ALL: 전체 일정
    THIS: 이 일정만
    THIS_AND_FOLLOWING: 이 일정과 이후 모든 일정
    
    주의: 반복 일정인 경우 필수''')