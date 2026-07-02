from pydantic import BaseModel

#pydantic validation for structured and stronger validation

class Component(BaseModel):
    """Represents a named component identified during code analysis."""

    name: str
    description: str


class CodeAnalysis(BaseModel):
    """Structured output produced by the code analysis stage."""

    language: str
    purpose: str
    execution_flow: str
    components: list[Component]
    potential_bugs: list[str]
    edge_cases: list[str]
    performance: str
    security: str
    code_quality: str
    improvements: list[str]
