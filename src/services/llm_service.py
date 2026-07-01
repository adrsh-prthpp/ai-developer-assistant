import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


DEFAULT_TEMPERATURE = 0.2

load_dotenv()


def get_llm() -> ChatOpenAI:
    """Create a configured OpenAI chat model for the assistant pipeline."""
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-5")

    if not api_key:
        raise ValueError("OPENAI_API_KEY is required.")

    return ChatOpenAI(
        model=model,
        temperature=DEFAULT_TEMPERATURE,
        api_key=api_key,
    )
