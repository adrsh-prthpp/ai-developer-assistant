# AI Developer Assistant

AI Developer Assistant is a Python CLI tool that analyzes source code with an LLM and generates professional Markdown documentation for developers.

## Features

* Accept code pasted into the terminal or loaded from a source file.
* Analyze code with LangChain and OpenAI.
* Validate structured analysis with Pydantic.
* Generate Markdown documentation from the validated analysis.
* Optionally save documentation to the `output/` directory.
* Ask session-only follow-up questions about the analyzed code and generated documentation.

## Architecture

```text
User Input
    |
    v
Code Analysis Agent
    |
    v
Pydantic Structured Validation
    |
    v
Documentation Agent
    |
    v
Markdown Output
    |
    v
Optional Follow-Up Assistant
```

## Setup

Create and activate a virtual environment, then install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file from `.env.example` and add your OpenAI API key:

```text
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-5
```

## Usage

Run the interactive CLI:

```bash
python -m src.main
```

Paste code directly:

```bash
python -m src.main --paste
```

Load code from a file:

```bash
python -m src.main --file sample_code/bank_account.py
```

Save generated documentation:

```bash
python -m src.main --file sample_code/bank_account.py --save
```

Generated Markdown files are written to `output/`.

## Follow-Up Questions

After documentation is generated, the CLI can answer clarification questions during the same session. The follow-up assistant uses only in-memory LangChain message history and does not persist conversation data.

## Project Structure

```text
src/
  agents/       LLM-backed analysis, documentation, and follow-up agents
  models/       Pydantic schemas
  prompts/      Reusable LangChain prompt templates
  services/     Shared LLM initialization
  main.py       CLI entry point
sample_code/    Example source files
tests/          Unit tests
output/         Generated documentation output
```

## Testing

Run the unit tests:

```bash
python -m unittest discover -s tests
```
