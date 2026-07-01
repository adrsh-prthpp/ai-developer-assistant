from pydantic import ValidationError

from src.models.schemas import CodeAnalysis
from src.prompts.analyzer_prompt import analysis_prompt
from src.services.llm_service import get_llm


def analyze_code(code: str) -> CodeAnalysis:
    """Analyze source code and return validated structured analysis."""
    if not code or not code.strip():
        raise ValueError("Code input cannot be empty.")

    structured_llm = get_llm().with_structured_output(CodeAnalysis)
    analysis_chain = analysis_prompt | structured_llm

    try:
        result = analysis_chain.invoke({"code_snippet": code})
    except ValidationError as exc:
        raise ValueError("LLM returned invalid code analysis output.") from exc

    if not isinstance(result, CodeAnalysis):
        raise TypeError("LLM response could not be parsed into a CodeAnalysis object.")

    return result
