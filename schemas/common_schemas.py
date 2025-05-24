from typing import Optional

from pydantic import BaseModel, Field


class Time(BaseModel):
    """일정 시간 정보"""
    start_at: str = Field(..., description='''일정 시작 시각, 5분 간격으로 설정 가능.
    UTC*, RFC5545의 DATE-TIME 형식(예: 2022-05-17T12:00:00Z)
    주의: all_day가 true인 경우 YYYY-MM-DDT00:00:00Z으로 설정(다른 값 설정 시 에러 발생)''')
    end_at: str = Field(..., description='''일정 종료 시각, start_at과 같은 형식, start_at 보다 미래 시점의 값
    주의: all_day가 true인 경우 YYYY-MM-DDT00:00:00Z으로 설정(다른 값 설정 시 에러 발생)''')
    time_zone: Optional[str] = Field("Asia/Seoul", description="타임존 설정, UTC*, RFC5545의 TZID 형식(기본값: Asia/Seoul)")
    all_day: Optional[bool] = Field(False, description="종일 일정 여부(기본값: false)")
    lunar: Optional[bool] = Field(False, description="날짜 기준을 음력으로 설정(기본값: false)")


class Location(BaseModel):
    """일정 장소 정보"""
    name: str = Field(None, max_length=100, description="장소 이름 (최대 100자)")
    location_id: Optional[int] = Field(None, description="장소 ID")
    address: Optional[str] = Field(None, description="주소")
    latitude: Optional[float] = Field(None, description="위도")
    longitude: Optional[float] = Field(None, description="경도")
