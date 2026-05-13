from langgraph.graph import END, START, MessagesState, StateGraph
from langchain.messages import AnyMessage, SystemMessage
from typing_extensions import TypedDict, Annotated
import operator
import os
from typing import Sequence
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from langchain_openrouter import ChatOpenRouter
from langchain_core.language_models import BaseChatModel
from dotenv import load_dotenv, find_dotenv
from src.lg_exc.stage_01.tools import multiply
from src.lg_exc.utils.graph_viz import save_graph_image
load_dotenv(find_dotenv())




def create_llm(model: str | None = None) -> BaseChatModel:
    """Create an LLM model."""
    if model is None:
        model = "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free"
    return ChatOpenRouter(model=model, temperature=0.4, api_key=os.getenv("OPENROUTER_API_KEY"))

Messages = Sequence[BaseMessage]

def demo_tool_binding() -> None:
    """ Only calls the tool needed but doesn't executes them"""
    llm = create_llm()
    llm_with_tools = llm.bind_tools([multiply])
    response = llm_with_tools.invoke(
        [HumanMessage(content="What is 45 multiplied by 62?")]
    )
    print(response)

def tool_calling_app(*, model:str | None = None):
    """ Create a compiled graph that routes messages through the LLM."""
    llm = create_llm(model = model)
    llm_with_tools = llm.bind_tools([multiply])

    def llm_node(state: MessagesState):
        response = llm_with_tools.invoke(state["messages"])
        return {"messages":[response]}

    graph = StateGraph(MessagesState)
    graph.add_node("tool_calling_llm", llm_node)
    graph.add_edge(START,"tool_calling_llm")
    graph.add_edge("tool_calling_llm",END)
    return graph.compile()


def main() -> None:
    demo_tool_binding()
    app = tool_calling_app()
    save_graph_image(app, filename="artifacts/agent_with_tool_call.png")

if __name__ == "__main__":
    main()