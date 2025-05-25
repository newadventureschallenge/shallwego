import os

from dotenv import load_dotenv
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableConfig
from langfuse.callback import CallbackHandler

from agent.agent_graph import get_graph
from agent.agent_state import initialize_sqlite_memory
from schemas.chat_schemas import ChatRequest
from utils import api_endpoints
from utils.custom_logger import setup_logger
from utils.filtering import is_filtered

load_dotenv()
router = APIRouter(prefix="", tags=["chat"])

logger = setup_logger(__name__)

@router.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket 연결을 처리합니다."""
    await websocket.accept()

    all_responses = []

    try:
        # 클라이언트가 보낸 JSON 수신
        payload = await websocket.receive_json()
        # Pydantic 모델로 변환
        req = ChatRequest(**payload)

        if await is_filtered(req.message):
            await websocket.send_json({"error": "Filtered content detected."})
            await websocket.close()
            return

        langfuse_handler = CallbackHandler(
            secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
            public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
            host=api_endpoints.LANGFUSE_HOST,
            session_id=req.user_id,
            user_id=req.user_id
        )

        config = RunnableConfig(
            recursion_limit=100,
            configurable={"thread_id": req.user_id},  # 스레드 ID 설정
            callbacks=[langfuse_handler]
        )

        graph = get_graph('chatbot-agent')  # 그래프 가져오기

        async for chunk, meta in graph.astream(
                input={
                    "access_token": req.access_token,
                    "messages": req.message,
                    "model_id": req.model_id
                },
                stream_mode="messages",
                config=config
        ):
            if meta.get("langgraph_node") == "trimmed_messages":
                continue

            # chunk.content 가 비어있지 않으면 그대로 내보냄
            if isinstance(chunk, ToolMessage):
                continue

            content = getattr(chunk, "content", None)
            if content:
                await websocket.send_json({"messages": content})  # 각 청크를 그대로 전달
                all_responses.append(content)

        await websocket.close()

    except WebSocketDisconnect:
        pass

    except Exception as e:
        logger.error(f"Error in WebSocket connection: {e}")
        await websocket.send_json({"error": str(e)})
        await websocket.close()

    finally:
        full_response = "".join(all_responses) if all_responses else "No response"
        logger.info(f"User: {getattr(req, 'user_id', 'unknown')} | Request: {getattr(req, 'message', '')[:100]} | Response: {full_response[:150]}...")


@router.delete('/reset')
async def reset_chat_log(
        user_id: str
):
    """
    SqliteSaver에 적재된 전체 채팅 로그를 삭제합니다.
    """
    saver = await initialize_sqlite_memory()
    await saver.adelete_thread(user_id)

    return {'status': 'success', 'message': 'Chat log reset successfully.'}
