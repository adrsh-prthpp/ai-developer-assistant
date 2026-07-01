import unittest
from unittest.mock import patch

from src.agents import documenter
from src.models.schemas import CodeAnalysis, Component


class FakeMessage:
    content = "# Code Summary\n\nGenerated documentation."


class FakeLLM:
    pass


class FakeChain:
    def invoke(self, inputs: object) -> FakeMessage:
        return FakeMessage()


class FakePrompt:
    def __or__(self, other: object) -> FakeChain:
        assert isinstance(other, FakeLLM)
        return FakeChain()


def make_analysis() -> CodeAnalysis:
    return CodeAnalysis(
        language="Python",
        purpose="Demonstrates a bank account.",
        execution_flow="Methods update the account balance.",
        components=[
            Component(
                name="BankAccount",
                description="Stores and updates an account balance.",
            )
        ],
        potential_bugs=[],
        edge_cases=["Negative withdrawals are not rejected."],
        performance="Constant-time balance updates.",
        security="No sensitive data handling is shown.",
        code_quality="Readable and compact.",
        improvements=["Validate withdrawal amounts."],
    )


class GenerateDocumentationTests(unittest.TestCase):
    def test_generate_documentation_returns_markdown(self) -> None:
        with (
            patch.object(documenter, "get_llm", return_value=FakeLLM()),
            patch.object(documenter, "documentation_prompt", FakePrompt()),
        ):
            result = documenter.generate_documentation(make_analysis())

        self.assertTrue(result.startswith("# Code Summary"))

    def test_generate_documentation_requires_code_analysis(self) -> None:
        with self.assertRaisesRegex(TypeError, "CodeAnalysis instance"):
            documenter.generate_documentation("not analysis")  # type: ignore[arg-type]
