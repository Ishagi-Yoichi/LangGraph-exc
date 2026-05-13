from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openrouter import ChatOpenRouter
from langchain_core.language_models import BaseChatModel
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def create_llm(model: str | None = None) -> BaseChatModel:
    """Create an LLM model."""
    if model is None:
        model = "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free"
    return ChatOpenRouter(model=model, temperature=0.4, api_key=os.getenv("OPENROUTER_API_KEY"))

def run_basic_chat(model: str | None = None) -> None:
    """Run a basic chat with the model."""
    llm = create_llm(model)
    response = llm.invoke([HumanMessage(content="Hello, how are you?")])
    print(response.content)

def main():
    run_basic_chat()

if __name__ == "__main__":
    main()