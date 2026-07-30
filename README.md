# AI Developer Assistant

A Python CLI that analyzes source code with an LLM, validates the analysis with
Pydantic, and generates structured Markdown documentation. Users can paste code,
load a source file, save the output, and ask follow-up questions within the
current session.

## Features

- Interactive, paste, and file-input modes
- Separate analyzer, documenter, and follow-up agents
- Structured Pydantic validation between agent stages
- Markdown generation with optional file output
- Example Python inputs
- Unit tests for analyzer, documenter, and CLI utility behavior

## Architecture

```text
Source input
  -> analyzer agent
  -> validated analysis model
  -> documenter agent
  -> Markdown output
  -> optional follow-up agent
```

The separation under `src/agents`, `src/prompts`, `src/models`, and
`src/services` keeps orchestration, prompts, schemas, and provider configuration
independent.

## Tech stack

- Python 3.11+
- LangChain and LangGraph
- OpenAI API
- Pydantic
- Pytest

## Installation

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Add `OPENAI_API_KEY` to `.env`. The committed example contains placeholders only.

## Usage

```bash
python -m src.main
python -m src.main --paste
python -m src.main --file sample_code/factorial.py
```

## Testing

```bash
pytest
```

Tests that invoke model-backed behavior may require a configured API key or
mocked provider.

## Project status

**Functional prototype.** Python syntax validation passes across the repository.
The project has a clear modular structure and tests, but it still depends on a
live model provider and does not yet include CI.

## Screenshot / demo

Add a terminal GIF showing source input, validated analysis, generated Markdown,
and a follow-up question.

## Future improvements

- Add offline provider mocks and deterministic integration tests
- Add GitHub Actions for linting and tests
- Stream long responses and expose token/cost estimates
- Support repository-level analysis with explicit file-size limits
- Add additional output formats such as JSON and HTML
