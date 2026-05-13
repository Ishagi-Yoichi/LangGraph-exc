from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openrouter import ChatOpenRouter
from langchain_core.language_models import BaseChatModel
from src.lg_exc.stage_01.tools import multiply
from src.lg_exc.utils.graph_viz import save_graph_image
import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
TOOLS =[multiply]

def create_llm(model: str | None = None) -> BaseChatModel:
    """Create an LLM model."""
    if model is None:
        model = "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free"
    return ChatOpenRouter(model=model, temperature=0.4, api_key=os.getenv("OPENROUTER_API_KEY"))

def _assemble_tool_router_graph(llm):
    """ Return compiled tool-router graph using provided llm."""
    llm_with_tools = llm.bind_tools(TOOLS)

    def tool_calling_llm(state: MessagesState):
        return {"messages": [llm_with_tools.invoke(state["messages"])]}

    graph = StateGraph(MessagesState)
    graph.add_node("tool_calling_llm", tool_calling_llm)
    graph.add_node("tools", ToolNode(TOOLS))
    graph.add_edge(START, "tool_calling_llm")
    graph.add_conditional_edges("tool_calling_llm", tools_condition)
    graph.add_edge("tools", END)
    return graph.compile()


def build_tool_calling_graph(*, model: str | None = None):
    """ Create a compiled stategraph configured for tool routing"""
    llm = create_llm(model=model)
    return _assemble_tool_router_graph(llm)

def run_demo(graph) -> None:
    """Run a small demo conversation through the compiled graph."""
    messages = [HumanMessage(content="Hello, what is 253523523 multiplied by 2321316?")]
    result = graph.invoke({"messages": messages})
    print(result["messages"])


def main() -> None:
    
    graph = build_tool_calling_graph()
    save_graph_image(graph, filename="artifacts/agent_with_tool_router.png")
    run_demo(graph)


if __name__ == "__main__":
    main()
