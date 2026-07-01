from langchain_core.prompts import PromptTemplate


documentation_prompt = PromptTemplate.from_template(
    """You are a technical documentation writer creating professional Markdown documentation for developers.

Use the validated CodeAnalysis object below as the sole source of truth. Convert it into concise, clear, developer-facing documentation.

The Markdown document must use exactly these sections:

# Code Language

# Code Summary

## Purpose

## How It Works

## Component Breakdown

## Error Handling & Edge Cases

## Performance & Security

## Suggested Improvements

## Example Use Cases

## Quick Summary

Write in a professional tone suitable for project documentation. Keep explanations concise and practical.
Do not include placeholder content. Do not mention missing information unless it is directly reflected in the analysis.

Validated CodeAnalysis object:
{code_analysis}
"""
)
