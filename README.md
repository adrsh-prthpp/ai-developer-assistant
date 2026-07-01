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

The AI Developer Assistant supports multiple ways to provide source code for analysis.

### Interactive Mode (Recommended)

Launch the interactive CLI. You will be prompted to either paste source code into the terminal or provide the path to a source file.

```bash
python -m src.main
```

### Paste Mode

Launch the CLI and paste your source code directly into the terminal. When finished, type `END` on a new line.

```bash
python -m src.main --paste
```

### File Mode

Analyze a source file directly without using the interactive menu.

```bash
python -m src.main --file sample_code/your_file.py
```

### Save Generated Documentation

Automatically save the generated Markdown documentation to the `output/` directory.

```bash
python -m src.main --file sample_code/your_file.py --save
```

Generated Markdown files are saved in the `output/` directory.


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
