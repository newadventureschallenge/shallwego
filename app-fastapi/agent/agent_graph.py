from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from agent.agent_nodes import inference_node, trimmed_message
from agent.agent_state import State, initialize_sqlite_memory
from agent.agent_tools import tools


agent_graphs = {}


async def build_chatbot_graph(name: str):
    """
    그래프를 빌드하고 반환합니다.
    """
    # 기본 그래프 생성
    graph_builder = StateGraph(State)

    graph_builder.add_node("trimmed_messages", trimmed_message)
    graph_builder.add_node("chatbot", inference_node)
    graph_builder.add_node("tools", ToolNode(tools))  # 웹 검색 도구 노드 추가

    graph_builder.add_edge(START, "trimmed_messages")
    graph_builder.add_edge("trimmed_messages", "chatbot")
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
