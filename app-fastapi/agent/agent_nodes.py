"""
에이전트 그래프 개별 노드 정의
"""
import os
from datetime import datetime
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from langchain_core.messages import trim_messages, SystemMessage, AIMessage, ToolMessage
from langchain_core.messages.utils import count_tokens_approximately
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import SystemMessagePromptTemplate
from langchain_core.runnables import RunnableConfig
from langfuse import Langfuse
from langgraph.graph.message import RemoveMessage, REMOVE_ALL_MESSAGES
from pydantic import BaseModel, Field

from agent.agent_llm import get_llm
from agent.agent_state import State
from core.db_session import get_session
from crud.prompt_crud import get_prompt
from data.vector_store import vector_store
from utils import api_endpoints

load_dotenv()

langfuse = Langfuse(
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    host=api_endpoints.LANGFUSE_HOST,
)

def get_system_message(key: str, model_id: str, nickname: str):
    """현재 서울 표준시를 기준으로 시스템 메시지를 생성합니다."""
    now = datetime.now(ZoneInfo("Asia/Seoul"))
    date_str = now.strftime("%Y-%m-%d %H:%M")

    with get_session() as session:
        system_prompt = get_prompt(session, key, model_id)

    system_msg_template = SystemMessagePromptTemplate.from_template(
        template=system_prompt.prompt,
        input_variables=["date_str", "nickname"],
    )

    return system_msg_template.format(date_str=date_str, nickname=nickname)

async def inference(state: State):
    """스트리밍 llm 호출 노드"""
    message = None
    llm = get_llm(state.model_id)

    # 만약 시스템 메시지가 없다면
    if not state.messages or not any(isinstance(msg, SystemMessage) for msg in state.messages):
        system_message = get_system_message('agent-chatbot', state.model_id, state.nickname)
        state.messages.insert(0, system_message)

    async for chunk in llm.astream(state.messages):
        message = chunk if message is None else message + chunk
        if chunk.content:
            yield {"messages": [chunk]}  # 각 청크를 그대로 전달

    yield {"messages": message}


def trimmed_message(state: State):
    # 만약 토큰이 10만개 이상이라면
    if count_tokens_approximately(state.messages) < 100000:
        return {}

    # llm에게 지금까지의 내용을 요약 부탁함
    llm = get_llm(state.model_id, False)

    conversation_txt = "\n".join(
        f"{m.role}: {m.content}" for m in state.messages
    )

    summary_prompt = (
        "다음 대화를 핵심 정보만 남기고 2000자 이내(한국어)로 간략히 요약해 주세요.\n\n"
        f"{conversation_txt}"
    )

    # llm.invoke() → ChatCompletion 메시지가 반환됨 (content 속성 보장)
    summary_result = llm.invoke(summary_prompt)
    summary_content = getattr(summary_result, "content", str(summary_result))
    summary_msg = AIMessage(content=f"지금까지의 대화 요약({datetime.now():%Y-%m-%d %H:%M}):\n{summary_content}")

    trimmed = trim_messages(
        state.messages,
        strategy="last",
        max_tokens=10000,
        token_counter=count_tokens_approximately,
        include_system=True,
    )
    trimmed = trimmed + [summary_msg]

    return {"messages": [RemoveMessage(REMOVE_ALL_MESSAGES)] + trimmed}


async def rag_recommendation(state: State):
    """
    RAG 추천 데이터 노드
    """
    results = vector_store.search(state.messages[-1].content)
    if results:
        # 결과를 가독성 있게 포맷팅
        formatted_results = "\n\n".join([f"• {result}" for result in results])
        return{"messages": [f"사용자 질문 기반 추가 정보:\n{formatted_results}"]}

    return {}


async def scoring(state: State, *, config: RunnableConfig):
    """
    답변 점수 매기기 노드
    """
    with get_session() as session:
        system_prompt = get_prompt(session, 'scoring', state.model_id)

    system_msg_template = SystemMessagePromptTemplate.from_template(
        template=system_prompt.prompt,
        input_variables=["conversation", "parser"],
    )

    N = 5  # 최근 5개 메시지만 사용
    recent_messages = state.messages[-N:] if len(state.messages) > N else state.messages

    # 구조화된 출력을 위한 스키마 정의
    class ConversationScore(BaseModel):
        score: int = Field(description="대화 만족도 점수 (0-100 사이의 정수)")

    parser = PydanticOutputParser(pydantic_object=ConversationScore)

    # 대화 내용 문자열 변환
    conversation_text = "\n".join([f"{msg.type}: {msg.content}" for msg in recent_messages])

    llm = get_llm(state.model_id, False)
    system_message = system_msg_template.format(conversation=conversation_text, parser=parser.get_format_instructions())

    result_text = await llm.ainvoke([system_message])
    result = parser.parse(result_text.content) if result_text.content else None

    # None 체크를 포함한 안전한 접근 방법
    score_value = result.score if result else 0
    langfuse.score(
        # trace_id=config.run_id,
        name="agent-score",
        value=score_value,
        dataType="NUMERIC"
    )

    return {}
