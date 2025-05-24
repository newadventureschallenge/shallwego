from typing import Annotated

from langgraph.graph import add_messages
from pydantic import BaseModel


class State(BaseModel):
    """
    graph 상태 모델 정의
    """
    access_token: str = ""  # 액세스 토큰
    messages: Annotated[list, add_messages]    # 메시지 정의(list type 이며 add_messages 함수를 사용하여 메시지를 추가)
