from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableConfig

from agent.agent_graph import graph
from schemas.chat_schemas import ChatRequest

router = APIRouter(prefix="", tags=["chat"])

@router.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket 연결을 처리합니다."""
    await websocket.accept()

    try:
        # 클라이언트가 보낸 JSON 수신
        payload = await websocket.receive_json()
        # Pydantic 모델로 변환
        req = ChatRequest(**payload)

        config = RunnableConfig(
            recursion_limit=10,  # 최대 10개의 노드까지 방문. 그 이상은 RecursionError 발생
            configurable={"thread_id": req.user_id},  # 스레드 ID 설정
        )

        async for chunk, _ in graph.astream(
                input={"access_token": req.access_token, "messages": req.message},
                stream_mode="messages",
                config=config
        ):
            # chunk.content 가 비어있지 않으면 그대로 내보냄
            if isinstance(chunk, ToolMessage):
                continue

            content = getattr(chunk, "content", None)
            if content:
                await websocket.send_json({"messages": content})  # 각 청크를 그대로 전달

        await websocket.close()

    except WebSocketDisconnect:
        pass
