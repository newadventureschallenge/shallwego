from typing import Annotated

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.constants import START, END
from langgraph.graph import add_messages, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from pydantic import BaseModel

from agent_tools import tools

load_dotenv()

# llm 모델 생성
llm = ChatOpenAI(model="gpt-4.1-mini")
llm_with_tools = llm.bind_tools(tools)

class State(BaseModel):
    """
    graph 상태 모델 정의
    """
    messages: Annotated[list, add_messages]    # 메시지 정의(list type 이며 add_messages 함수를 사용하여 메시지를 추가)

# 챗봇 함수 정의
async def inference_node(state: State):
    """스트리밍 llm 호출 노드"""
    message = None

    async for chunk in llm_with_tools.astream(state.messages):
        message = chunk if message is None else message + chunk
        if chunk.content:
            yield {"messages": [chunk]}  # 각 청크를 그대로 전달

    yield {"messages": message}

# 기본 그래프 생성
graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", inference_node)
graph_builder.add_node("tools", ToolNode(tools))  # 웹 검색 도구 노드 추가

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()
