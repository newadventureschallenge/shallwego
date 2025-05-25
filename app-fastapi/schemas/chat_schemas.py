from pydantic import BaseModel


class ChatRequest(BaseModel):
    """
    채팅 요청 스키마
    """
    message: str
    user_id: str
    access_token: str
    model_id: str
