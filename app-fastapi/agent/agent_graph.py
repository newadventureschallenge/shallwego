from datetime import datetime
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from agent.agent_state import State, initialize_sqlite_memory
from agent.agent_tools import tools

load_dotenv()

# llm 모델 생성
llm = ChatOpenAI(model="gpt-4.1-mini")
llm_with_tools = llm.bind_tools(tools)

agent_graphs = {}


# 챗봇 함수 정의
async def inference_node(state: State):
    """스트리밍 llm 호출 노드"""
    # 1) 서울 표준시로 현재 시각 얻기
    now = datetime.now(ZoneInfo("Asia/Seoul"))
    date_str = now.strftime("%Y-%m-%d %H:%M")

    # 2) 동적 시스템 메시지 생성
    system_msg = SystemMessage(
        content=f"지금 시간은 {date_str} 입니다. 이후 대화를 이 날짜 기준으로 처리해 주세요."
    )

    # 3) 메시지 리스트 맨 앞에 삽입
    all_messages = [system_msg] + state.messages

    message = None

    async for chunk in llm_with_tools.astream(all_messages):
        message = chunk if message is None else message + chunk
        if chunk.content:
            yield {"messages": [chunk]}  # 각 청크를 그대로 전달

    yield {"messages": message}


async def build_chatbot_graph(name: str):
    """
    그래프를 빌드하고 반환합니다.
    """
    # 기본 그래프 생성
    graph_builder = StateGraph(State)

    graph_builder.add_node("chatbot", inference_node)
    graph_builder.add_node("tools", ToolNode(tools))  # 웹 검색 도구 노드 추가

    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_conditional_edges("chatbot", tools_condition)
    graph_builder.add_edge("tools", "chatbot")
    graph_builder.add_edge("chatbot", END)

    memory = await initialize_sqlite_memory()

    graph = graph_builder.compile(checkpointer=memory)
    agent_graphs[name] = graph


def get_graph(name: str):
    """
    그래프를 반환합니다.
    """
    if name not in agent_graphs:
        raise ValueError(f"Graph '{name}' not found. Please build the graph first.")

    return agent_graphs[name]
