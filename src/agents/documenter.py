from src.models.schemas import CodeAnalysis
from src.prompts.documenter_prompt import documentation_prompt
from src.services.llm_service import get_llm


def generate_documentation(analysis: CodeAnalysis) -> str:
    """Generate Markdown documentation from a validated code analysis."""
    if not isinstance(analysis, CodeAnalysis):
        raise TypeError("analysis must be a CodeAnalysis instance.")

    documentation_chain = documentation_prompt | get_llm()
    response = documentation_chain.invoke(
        {"code_analysis": analysis.model_dump_json(indent=2)}
    )

    if isinstance(response, str):
        return response

    content = getattr(response, "content", None)
    if isinstance(content, str):
        return content

    raise TypeError("LLM response could not be converted into Markdown text.")
