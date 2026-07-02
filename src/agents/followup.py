from langchain_core.messages import BaseMessage

from src.prompts.followup_prompt import followup_prompt
from src.services.llm_service import get_llm


def answer_followup(session_messages: list[BaseMessage]) -> str: #takes in session history list
    """Answer a follow-up question using the current session message history."""
    if not session_messages:
        raise ValueError("Session message history cannot be empty.")

    followup_chain = followup_prompt | get_llm()
    response = followup_chain.invoke({"session_messages": session_messages})

    if isinstance(response, str):
        return response

    content = getattr(response, "content", None)
    if isinstance(content, str):
        return content

    raise TypeError("LLM response could not be converted into follow-up text.")
