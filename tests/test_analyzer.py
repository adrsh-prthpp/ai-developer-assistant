import unittest
from unittest.mock import patch

from src.agents import analyzer
from src.models.schemas import CodeAnalysis, Component


class FakeStructuredLLM:
    pass


class FakeChain:
    def invoke(self, inputs: object) -> CodeAnalysis:
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

#tests analyzer function with mock LLM
class FakeLLM:
    def with_structured_output(self, schema: type[CodeAnalysis]) -> FakeStructuredLLM:
        assert schema is CodeAnalysis
        return FakeStructuredLLM()


class FakePrompt:
    def __or__(self, other: object) -> FakeChain:
        assert isinstance(other, FakeStructuredLLM)
        return FakeChain()


class AnalyzeCodeTests(unittest.TestCase):
    def test_analyze_code_returns_valid_analysis(self) -> None:
        with (
            patch.object(analyzer, "get_llm", return_value=FakeLLM()),
            patch.object(analyzer, "analysis_prompt", FakePrompt()),
        ):
            result = analyzer.analyze_code("class BankAccount: pass")

        self.assertIsInstance(result, CodeAnalysis)
        self.assertEqual(result.components[0].name, "BankAccount")

    def test_analyze_code_rejects_empty_input(self) -> None:
        with self.assertRaisesRegex(ValueError, "Code input cannot be empty"):
            analyzer.analyze_code("  ")
