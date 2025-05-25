from typing import Annotated

import aiosqlite
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.graph import add_messages
from pydantic import BaseModel


class State(BaseModel):
    """
    graph 상태 모델 정의
    """
    access_token: str = ""  # 액세스 토큰
    messages: Annotated[list, add_messages]    # 메시지 정의(list type 이며 add_messages 함수를 사용하여 메시지를 추가)
    model_id: str  # 모델 ID


async def initialize_sqlite_memory():
    """
    비동기 SQLite 데이터베이스 연결을 초기화하고 AsyncSqliteSaver 인스턴스를 반환합니다.
    """
    conn = await aiosqlite.connect("sqlite_checkpointer.sqlite")
    return AsyncSqliteSaver(conn)
