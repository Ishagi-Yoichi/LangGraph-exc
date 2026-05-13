from langchain.tools import tool
from langchain.chat_models import init_chat_model



@tool
def multiply(a: int, b: int) -> int:
    """Multiply 'a' and 'b' .

    Args:
        a: The first number to multiply
        b: The second number to multiply
    """
    return a * b

tools = [multiply]
tools_by_name = {tool.name: tool for tool in tools}
