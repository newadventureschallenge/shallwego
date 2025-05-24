"""
톡캘린더 할 일 관련 API 스키마 정의
"""

from typing import Optional

from pydantic import BaseModel, Field

class Recur(BaseModel):
    """할 일 반복 정보"""
    rrule: str = Field(..., description='''
할 일의 반복 주기, UTC*, RFC5545의 RRULE 형식
(예: FREQ=DAILY;UNTIL=20211208T155959Z)
UNTIL은 yyyyMMdd'T'000000Z형식으로 due_date 이후만 지정 가능하며 rrule 조건을 만족하는 날짜 하루 이상 필요''')
    record_on: Optional[bool] = Field(None, description="[도전 기록 보기] 활성화 여부. true: 활성화, false: 비활성화(기본값)")


class DueInfo(BaseModel):
    """할 일 기한 정보"""
    due_date: str = Field(..., description="기한 일자, yyyyMMdd 형식. 주의: 과거 시점으로 설정 불가")
    time_zone: Optional[str] = Field("Asia/Seoul", description="기한 일자의 타임존, UTC*, RFC5545의 TZID 형식(기본값: Asia/Seoul)")
    alarm_time: Optional[str] = Field(None, description="알림 시각, 5분 간격의 HHmm 형식(단위: 분, 기본값: 알림 없음)")
    recur: Optional[Recur] = Field(None, description="할 일의 반복 정보(기본값: 반복 없음)")


class Task(BaseModel):
    """할 일 정보"""
    content: str = Field(..., max_length=1000, description="내용(최대 1,000자)")
    bookmark: Optional[bool] = Field(None, description="즐겨찾기 여부(기본값: false). 중요-할 일 수정에만 사용")
    due_info: Optional[DueInfo] = Field(None, description="기한 일자 정보(기본값: 기한 없음)")


class RequestCreateTask(BaseModel):
    """할 일 생성하기"""
    task: Task = Field(..., description="할 일 정보")


class RequestGetTasks(BaseModel):
    """할 일 조회하기
    기간으로 조회하려면 task_id 파라미터를 제외하고 from, to 파라미터를 사용해야 합니다.
    """
    task_id: Optional[str] = Field(..., description="할 일 ID. <주의: 해당 파라미터 포함 시 ID에 해당하는 할 일 단건만 조회하며, 다른 요청 파라미터는 모두 무시됨>")
    from_: Optional[str] = Field(None, alias="from", description="조회 기간의 시작 시각, yyyyMMdd 형식. 중요: task_id 미포함 시 필수")
    to: Optional[str] = Field(None, description="조회 기간의 종료 시각, yyyyMMdd 형식. from 이후 31일 이내의 값. 중요: task_id 미포함 시 필수")
    task_status: Optional[str] = Field(None, description="조회할 할 일 상태. 아래 중 하나. COMPLETED: 완료, TODO: 미완료(기본값), ALL: 전체(TODO 상태 우선 표시)")
    task_filter: Optional[str] = Field(None, description='''
조회할 할 일 조건(기본값: 전체 할 일 조회)
쉼표(",")를 구분자로 여러 값 전달 가능(예: "authorized,bookmark"), 아래 중 하나
authorized: 수정 또는 삭제 가능한 할 일
bookmark: 즐겨찾기에 추가한 할 일''')
    offset: Optional[int] = Field(0, description="조회 결과 목록 시작 지점(기본값: 0)")
    limit: Optional[int] = Field(100, ge=1, le=1000, description="	페이지당 결과 수(기본값: 100, 최대 1000)")
    time_zone: Optional[str] = Field("Asia/Seoul", description="기한 일자의 타임존, UTC*, RFC5545의 TZID 형식(기본값: Asia/Seoul). 중요: 응답의 status 시각 계산 기준")

    class Config:
        validate_by_name = True
        allow_population_by_alias = True


class RequestTaskRecords(BaseModel):
    """도전 기록 보기"""
    task_id: str = Field(..., description="할 일 ID")
    from_: Optional[str] = Field(None, alias="from", description="조회 기간의 시작 시각, yyyyMMdd 형식")
    to: Optional[str] = Field(None, description="조회 기간의 종료 시각, yyyyMMdd 형식")

    class Config:
        validate_by_name = True
        allow_population_by_alias = True


class RequestUpdateTask(BaseModel):
    """할 일 수정하기"""
    task_id: str = Field(..., description="할 일 ID")
    task: Task = Field(..., description="할 일 정보")


class RequestCompleteTask(BaseModel):
    """할 일 완료하기"""
    task_id: str = Field(..., description="할 일 ID")
    complete: bool = Field(..., description="할 일 완료 여부. true: 완료, false: 미완료")


class RequestDeleteTask(BaseModel):
    """할 일 삭제하기"""
    task_id: str = Field(..., description="할 일 ID")
