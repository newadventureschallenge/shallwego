from datetime import datetime
from zoneinfo import ZoneInfo

from langchain_core.messages import trim_messages, SystemMessage, AIMessage
from langchain_core.messages.utils import count_tokens_approximately
from langchain_core.prompts import SystemMessagePromptTemplate
from langgraph.graph.message import RemoveMessage, REMOVE_ALL_MESSAGES

from agent.agent_llm import get_llm
from agent.agent_state import State
from core.db_session import get_session
from crud.prompt_crud import get_prompt


def get_system_message(model_id: str):
    """현재 서울 표준시를 기준으로 시스템 메시지를 생성합니다."""
    now = datetime.now(ZoneInfo("Asia/Seoul"))
    date_str = now.strftime("%Y-%m-%d %H:%M")

    with get_session() as session:
        system_prompt = get_prompt(session, 'agent-chatbot', model_id)

    system_msg_template = SystemMessagePromptTemplate.from_template(
        template=system_prompt.prompt,
        input_variables=["date_str"],
    )

    return system_msg_template.format(date_str=date_str)

async def inference_node(state: State):
    """스트리밍 llm 호출 노드"""

    message = None
    llm = get_llm(state.model_id)

    # 만약 시스템 메시지가 없다면
    if not state.messages or not any(isinstance(msg, SystemMessage) for msg in state.messages):
        system_message = get_system_message(state.model_id)
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
    llm = get_llm(state.model_id)

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
