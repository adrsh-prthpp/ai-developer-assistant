from langchain_core.prompts import PromptTemplate


analysis_prompt = PromptTemplate.from_template(
    """You are a senior software engineer performing a comprehensive technical analysis of a code snippet.

Analyze the provided code carefully and return structured output that matches the CodeAnalysis Pydantic schema.

Your analysis must cover:
- Overall purpose
- High-level execution flow
- Component breakdown for functions, classes, modules, and other meaningful units
- Logic analysis, including important decisions, data transformations, and control flow
- Potential bugs
- Edge cases
- Performance considerations
- Security concerns
- Code quality
- Suggested improvements

Return only data that can be validated against this schema:
- language: string
- purpose: string
- execution_flow: string
- components: list of objects with name and description strings
- potential_bugs: list of strings
- edge_cases: list of strings
- performance: string
- security: string
- code_quality: string
- improvements: list of strings

Be precise, technical, and concise. Do not invent behavior that is not supported by the code.

Code snippet:
{code_snippet}
"""
)
