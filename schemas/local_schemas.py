"""
카카오 로컬 검색 API 스키마 정의
"""

from typing import Optional

from pydantic import BaseModel, Field

from utils.enums import CategoryGroupCode


class RequestLocalSearchKeyword(BaseModel):
    query: str = Field(..., description="검색을 원하는 질의어")
    category_group_code: Optional[CategoryGroupCode] = Field(..., description="카테고리 그룹 코드, 카테고리로 결과 필터링을 원하는 경우 사용")
    x: Optional[str] = Field(None, description="중심 좌표의 X 혹은 경도(longitude) 값. 특정 지역을 중심으로 검색할 경우 radius와 함께 사용 가능")
    y: Optional[str] = Field(None, description="중심 좌표의 Y 혹은 위도(latitude) 값. 특정 지역을 중심으로 검색할 경우 radius와 함께 사용 가능")
    radius: Optional[int] = Field(None, description="중심 좌표부터의 반경거리. 특정 지역을 중심으로 검색하려고 할 경우 중심좌표로 쓰일 x,y와 함께 사용 (단위: 미터(m), 최소: 0, 최대: 20000)")
    rect: Optional[str] = Field(None, description="사각형의 지정 범위 내 제한 검색을 위한 좌표. 지도 화면 내 검색 등 제한 검색에서 사용 가능. 좌측 X 좌표, 좌측 Y 좌표, 우측 X 좌표, 우측 Y 좌표 형식")
    page: Optional[int] = Field(1, ge=1, le=45, description="결과 페이지 번호 (최소: 1, 최대: 45, 기본값: 1)")
    size: Optional[int] = Field(15, ge=1, le=15, description="한 페이지에 보여질 문서 수 (최소: 1, 최대: 15, 기본값: 15)")
    sort: Optional[str] = Field("accuracy", description="결과 정렬 순서. distance 정렬을 원할 때는 기준 좌표로 쓰일 x, y와 함께 사용. distance 또는 accuracy(기본값: accuracy)")


class RequestLocalSearchCategory(BaseModel):
    category_group_code: CategoryGroupCode = Field(..., description="카테고리 그룹 코드")
    x: Optional[str] = Field(None, description="중심 좌표의 X 혹은 경도(longitude) 값. 특정 지역을 중심으로 검색할 경우 radius와 함께 사용 가능")
    y: Optional[str] = Field(None, description="중심 좌표의 Y 혹은 위도(latitude) 값. 특정 지역을 중심으로 검색할 경우 radius와 함께 사용 가능")
    radius: int = Field(..., ge=0, le=20000, description="중심 좌표부터의 반경거리. 특정 지역을 중심으로 검색하려고 할 경우 중심좌표로 쓰일 x,y와 함께 사용. 단위 meter, 0~20000 사이의 값")
    rect: Optional[str] = Field(None, description="사각형의 지정 범위 내 제한 검색을 위한 좌표. 지도 화면 내 검색 등 제한 검색에서 사용 가능. 좌측 X 좌표, 좌측 Y 좌표, 우측 X 좌표, 우측 Y 좌표 형식")
    page: Optional[int] = Field(1, ge=1, le=45, description="결과 페이지 번호 (최소: 1, 최대: 45, 기본값: 1)")
    size: Optional[int] = Field(15, ge=1, le=15, description="한 페이지에 보여질 문서 수 (최소: 1, 최대: 15, 기본값: 15)")
