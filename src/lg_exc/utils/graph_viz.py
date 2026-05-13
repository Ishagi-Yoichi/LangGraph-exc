
from pathlib import Path

from langgraph.graph.state import CompiledStateGraph


def save_graph_image( app: CompiledStateGraph , filename:str, xray=False):
    graph = app.get_graph(xray=xray)

    png_bytes = graph.draw_mermaid_png()

    output_path = Path(filename)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(png_bytes)

    print(f"Graph saved to {output_path}")
    return output_path