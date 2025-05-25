"""
채팅 요청 스키마 정의
"""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    채팅 요청 스키마
    """
    message: str = Field(..., description="사용자 입력 메시지")
    nickname: str = Field(..., description="사용자 닉네임")
    user_id: str = Field(..., description="사용자 고유 ID")
    access_token: str = Field(..., description="사용자 액세스 토큰(암호화)")
    model_id: str = Field(..., description="사용할 모델 ID")
