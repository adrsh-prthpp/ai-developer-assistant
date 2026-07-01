import argparse
import sys
from pathlib import Path

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage

from src.agents.analyzer import analyze_code
from src.agents.documenter import generate_documentation
from src.agents.followup import answer_followup
from src.models.schemas import CodeAnalysis


WELCOME_MESSAGE = """========================================
AI Developer Assistant
========================================

Generate professional documentation for your source code.
"""


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the CLI."""
    parser = argparse.ArgumentParser(
        description="Generate professional Markdown documentation for source code."
    )
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument(
        "--paste",
        action="store_true",
        help="Paste source code into the terminal.",
    )
    input_group.add_argument(
        "--file",
        type=Path,
        help="Load source code from a file.",
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save the generated documentation to the output directory.",
    )
    return parser.parse_args()


def read_pasted_code() -> str:
    """Read pasted code until the user enters END on a new line."""
    print("Paste your source code below.\n")
    print("When you are finished, type END on a new line and press Enter.")

    lines: list[str] = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)

    code = "\n".join(lines)
    if not code.strip():
        raise ValueError("Pasted code cannot be empty.")

    return code


def read_file_code(file_path: Path) -> str:
    """Read source code from a validated file path."""
    if not file_path.exists():
        raise ValueError(f"File does not exist: {file_path}")
    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    code = file_path.read_text(encoding="utf-8")
    if not code.strip():
        raise ValueError(f"Source file is empty: {file_path}")

    return code


def choose_interactive_input() -> tuple[str, Path | None]:
    """Collect source code using the interactive prompt flow."""
    print("Choose an input method:\n")
    print("1. Paste code into the terminal")
    print("2. Load code from a source file\n")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        return read_pasted_code(), None
    if choice == "2":
        file_path = Path(input("Enter the file path: ").strip())
        return read_file_code(file_path), file_path

    raise ValueError("Invalid choice. Enter 1 to paste code or 2 to load a file.")


def save_documentation(markdown: str, source_file: Path | None) -> Path:
    """Save generated documentation to the output directory."""
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    if source_file is None:
        output_path = output_dir / "generated_documentation.md"
    else:
        output_path = output_dir / f"{source_file.stem}_documentation.md"

    output_path.write_text(markdown, encoding="utf-8")
    return output_path


def wants_followup() -> bool:
    """Ask whether the user wants clarification about the generated documentation."""
    choice = input(
        "Is there any part of the analysis or documentation you would like me to clarify? [y/N]: "
    ).strip().lower()
    return choice in {"y", "yes"}


def wants_another_question() -> bool:
    """Ask whether the user wants to continue the follow-up conversation."""
    choice = input("Do you have another question? [y/N]: ").strip().lower()
    return choice in {"y", "yes"}


def build_followup_session(
    code: str,
    analysis: CodeAnalysis,
    documentation: str,
) -> list[BaseMessage]:
    """Create session-only follow-up context for the current CLI run."""
    return [
        SystemMessage(
            content=(
                "Use the following session context to answer follow-up questions.\n\n"
                "Original source code:\n"
                f"{code}\n\n"
                "Validated CodeAnalysis object:\n"
                f"{analysis.model_dump_json(indent=2)}\n\n"
                "Generated Markdown documentation:\n"
                f"{documentation}"
            )
        )
    ]


def run_followup_conversation(
    code: str,
    analysis: CodeAnalysis,
    documentation: str,
) -> None:
    """Run the optional session-based follow-up conversation."""
    if not wants_followup():
        return

    session_messages = build_followup_session(code, analysis, documentation)

    while True:
        question = input("What would you like clarified? ").strip()
        if not question:
            print("Please enter a question so I can help clarify the documentation.")
            continue

        session_messages.append(HumanMessage(content=question))
        response = answer_followup(session_messages)
        session_messages.append(AIMessage(content=response))

        print()
        print(response)
        print()

        if not wants_another_question():
            break


def should_save_interactively() -> bool:
    """Ask whether generated documentation should be saved."""
    choice = input("Save documentation to a Markdown file? [y/N]: ").strip().lower()
    return choice in {"y", "yes"}


def main() -> int:
    """Run the AI Developer Assistant CLI."""
    args = parse_args()
    source_file: Path | None = None

    print(WELCOME_MESSAGE)

    try:
        if args.file is not None:
            source_file = args.file
            code = read_file_code(source_file)
        elif args.paste:
            code = read_pasted_code()
        else:
            code, source_file = choose_interactive_input()

        print("Analyzing code...")
        analysis = analyze_code(code)

        print("Generating documentation...")
        documentation = generate_documentation(analysis)

        print()
        print(documentation)
        print()

        run_followup_conversation(code, analysis, documentation)

        save_requested = args.save
        if not args.save and not args.file and not args.paste:
            save_requested = should_save_interactively()

        if save_requested:
            print("Saving documentation...")
            output_path = save_documentation(documentation, source_file)
            print(f"Documentation saved to: {output_path}")

        print("Done.")
        return 0
    except (OSError, TypeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
