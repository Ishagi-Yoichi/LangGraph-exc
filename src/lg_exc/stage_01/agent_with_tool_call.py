from langgraph.graph import END, START, MessagesState, StateGraph
from langchain.messages import AnyMessage, SystemMessage
from typing_extensions import TypedDict, Annotated
import operator

class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int

def mock_llm(state: MessagesState) -> MessagesState:
    return {"messages": [{"role": "ai", "content": "hello world"}]}

graph = StateGraph(MessagesState)
graph.add_node("llm",mock_llm)
graph.add_edge(START, "mock_llm")
graph.add_edge("mock_llm", END)

graph = graph.compile()

result = graph.invoke({"messages": [{"role": "user", "content": "What is the weather in Tokyo?"}]})
print(result)