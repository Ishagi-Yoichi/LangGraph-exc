import random
from typing import Literal

from langchain_core.runnables import RunnableConfig
from langgraph.constants import END, START
from langgraph.graph import StateGraph
from typing_extensions import TypedDict

from src.lg_exc.utils.graph_viz import save_graph_image

class State(TypedDict):
    graph_state: str

def introduce(state: str) -> State:
    print("------Introduce------")
    return {"graph_state":f"{state['graph_state']} I am"}

def happy_path(state: State) -> State:
    print("---Happy---")
    return {"graph_state": f"{state['graph_state']} happy!"}


def sad_path(state: State) -> State:
    print("---Sad---")
    return {"graph_state": f"{state['graph_state']} sad!"}


def decide_mood(_: State) -> Literal["happy", "sad"]:
    """Randomly choose the next node."""
    return random.choice(["happy", "sad"])

def build_graph():
    """ Construct a simple branching state graph."""
    graph = StateGraph(State)
    graph.add_node("introduce",introduce)
    graph.add_node("happy", happy_path)
    graph.add_node("sad", sad_path)

    graph.add_edge(START,"introduce")
    graph.add_conditional_edges("introduce",decide_mood)
    graph.add_edge("happy",END)
    graph.add_edge("sad",END)
    return graph.compile()

def visualize(app) -> None:
    """ Render the graph to a PNG file."""
    save_graph_image(app, filename="artifacts/agent_with_router.png")

def run_demo(app) -> None:
    """Invoke the graph with a sample state."""
    result = app.invoke({"graph_state": "Leslie"})
    print("Graph output:", result)

def main() -> None:
    app = build_graph()
    visualize(app)
    run_demo(app)

if __name__ == "__main__":
    main()
