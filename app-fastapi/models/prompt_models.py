"""
데이터베이스 내 프롬프트 모델을 정의합니다.
"""

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import SQLModel, Field


class SystemPrompt(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    key: str
    prompt: str
    model_id: str
    time_stamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    version: int = Field(default=1)
