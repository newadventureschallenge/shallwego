from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from agent.agent_graph import build_chatbot_graph
from core.db_session import init_db
from routers import chat_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        init_db()
        await build_chatbot_graph('chatbot-agent')
        yield
    finally:
        pass


app = FastAPI(
    title="shallwego backend",
    version="0.0.1",
    lifespan=lifespan,
    root_path="",
)

origins = [
    "http://localhost:8501",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router.router)


@app.get("/health")
async def health_check():
    """서버 헬스 체크 """
    return {"status": "ok"}


@app.get("/")
async def root():
    """루트 페이지"""
    return {"message": "Welcome to the shallwego backend!"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
