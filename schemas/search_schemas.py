from typing import Optional

from pydantic import BaseModel, Field


class WebSearchRequest(BaseModel):
    """웹 문서 검색하기"""
    query: str = Field(..., description="검색을 원하는 질의어")
    sort: Optional[str] = Field("accuracy", description="결과 문서 정렬 방식, accuracy(정확도순) 또는 recency(최신순), 기본 값 accuracy")
    page: Optional[int] = Field(1, ge=1, le=50, description="결과 페이지 번호, 1~50 사이의 값, 기본 값 1")
    size: Optional[int] = Field(30, ge=1, le=50, description="한 페이지에 보여질 문서 수, 1~50 사이의 값, 기본 값 10")
