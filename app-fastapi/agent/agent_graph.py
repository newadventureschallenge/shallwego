"""
LangGraph 기반의 챗봇 에이전트 그래프를 정의합니다.
"""

from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from agent.agent_nodes import inference, trimmed_message, rag_recommendation, scoring
from agent.agent_state import State, initialize_sqlite_memory
from agent.agent_tools import tools


agent_graphs = {}


async def build_chatbot_graph(name: str):
    """
    그래프를 빌드하고 반환합니다.
    """
    # 기본 그래프 생성
    # 그래프의 구조는 docs/phase2/agent_graph_mermaid.md 와 png 파일 참고
    graph_builder = StateGraph(State)

    graph_builder.add_node("rag_recommendation", rag_recommendation)
    graph_builder.add_node("trimmed_messages", trimmed_message)
    graph_builder.add_node("chatbot", inference)
    graph_builder.add_node("tools", ToolNode(tools))
    graph_builder.add_node("scoring", scoring)

    graph_builder.add_edge(START, "rag_recommendation")
    graph_builder.add_edge("rag_recommendation", "trimmed_messages")
    graph_builder.add_edge("trimmed_messages", "chatbot")
    graph_builder.add_conditional_edges(
        source="chatbot",
        path=tools_condition,
        path_map={
            "tools": "tools",
            "__end__": "scoring",
        })
    graph_builder.add_edge("tools", "chatbot")
    graph_builder.add_edge("scoring", END)

    memory = await initialize_sqlite_memory()

    graph = graph_builder.compile(checkpointer=memory)
    agent_graphs[name] = graph

    # 그래프를 Mermaid 형식으로 출력 (시각화 용도)
    # print(graph.get_graph().draw_mermaid())


def get_graph(name: str):
    """
    그래프를 반환합니다.
    """
    if name not in agent_graphs:
        raise ValueError(f"Graph '{name}' not found. Please build the graph first.")

    return agent_graphs[name]
