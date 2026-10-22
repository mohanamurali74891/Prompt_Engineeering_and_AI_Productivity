"""
Module 3: LLM APIs & Application Development
=============================================
structured_responses.py — Structured output helpers

Utilities for extracting, validating, and working with structured
(JSON) data from LLM responses.
"""

import json
import re
import logging
from typing import Any, Dict, List, Optional, Type, TypeVar
from dataclasses import dataclass

logger = logging.getLogger(__name__)

T = TypeVar("T")


# ─────────────────────────────────────────────────────────────
# JSON Extraction
# ─────────────────────────────────────────────────────────────

def extract_json(text: str) -> Optional[Any]:
    """
    Extract the first valid JSON object or array from a text string.

    The model sometimes wraps JSON in markdown code fences:
        ```json
        { ... }
        ```
    This function handles all common formats.

    Parameters
    ----------
    text : str
        Raw LLM response text.

    Returns
    -------
    Parsed Python object (dict, list, etc.) or None if no valid JSON found.

    Example
    -------
    >>> raw = '```json\\n{"name": "Alice", "age": 30}\\n```'
    >>> extract_json(raw)
    {'name': 'Alice', 'age': 30}
    """
    # 1. Try to strip markdown code fences
    fence_pattern = re.compile(r"```(?:json)?\s*([\s\S]*?)```", re.IGNORECASE)
    match = fence_pattern.search(text)
    if match:
        candidate = match.group(1).strip()
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass

    # 2. Try to find raw JSON object or array
    for pattern in [r"(\{[\s\S]*\})", r"(\[[\s\S]*\])"]:
        match = re.search(pattern, text)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                continue

    # 3. Try to parse the entire text
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        logger.warning("Could not extract valid JSON from response.")
        return None


def extract_json_strict(text: str, required_keys: Optional[List[str]] = None) -> Dict:
    """
    Extract JSON and optionally validate that required keys are present.

    Parameters
    ----------
    text : str
        Raw LLM response text.
    required_keys : list of str, optional
        Keys that must be present in the extracted JSON object.

    Returns
    -------
    dict

    Raises
    ------
    ValueError
        If JSON cannot be extracted or required keys are missing.
    """
    result = extract_json(text)
    if result is None:
        raise ValueError(f"No valid JSON found in response:\n{text[:200]}")
    if not isinstance(result, dict):
        raise ValueError(f"Expected a JSON object (dict), got {type(result).__name__}.")
    if required_keys:
        missing = [k for k in required_keys if k not in result]
        if missing:
            raise ValueError(f"JSON is missing required keys: {missing}")
    return result


# ─────────────────────────────────────────────────────────────
# Prompt builders for structured output
# ─────────────────────────────────────────────────────────────

def build_json_prompt(instruction: str, schema: Dict[str, str]) -> str:
    """
    Append a schema description to a prompt to encourage JSON output.

    Parameters
    ----------
    instruction : str
        The main task instruction.
    schema : dict
        Mapping of field names to descriptions.

    Returns
    -------
    str — the enriched prompt

    Example
    -------
    >>> prompt = build_json_prompt(
    ...     "Analyse the sentiment of this review: 'Great product!'",
    ...     {"sentiment": "positive|neutral|negative", "confidence": "0.0-1.0", "reason": "short explanation"}
    ... )
    """
    schema_lines = "\n".join(f'  "{k}": {v}' for k, v in schema.items())
    return (
        f"{instruction}\n\n"
        f"Respond ONLY with a valid JSON object matching this schema:\n"
        f"{{\n{schema_lines}\n}}\n"
        f"Do not include any text outside the JSON object."
    )


# ─────────────────────────────────────────────────────────────
# Pre-built structured response functions
# ─────────────────────────────────────────────────────────────

def sentiment_analysis_prompt(text: str) -> str:
    """Return a prompt that asks for structured sentiment analysis."""
    return build_json_prompt(
        f'Analyse the sentiment of the following text:\n\n"{text}"',
        {
            "sentiment": '"positive" | "neutral" | "negative"',
            "confidence": "number between 0.0 and 1.0",
            "emotions": "list of detected emotions (e.g. [\"joy\", \"surprise\"])",
            "reason": "one-sentence explanation",
        },
    )


def entity_extraction_prompt(text: str) -> str:
    """Return a prompt that asks for named entity extraction."""
    return build_json_prompt(
        f'Extract all named entities from the following text:\n\n"{text}"',
        {
            "persons": "list of person names",
            "organisations": "list of organisation names",
            "locations": "list of location names",
            "dates": "list of dates or time expressions",
            "other": "list of any other notable entities",
        },
    )


def summarise_prompt(text: str, max_words: int = 50) -> str:
    """Return a prompt that asks for a structured summary."""
    return build_json_prompt(
        f'Summarise the following text in at most {max_words} words:\n\n"{text}"',
        {
            "summary": f"concise summary in ≤{max_words} words",
            "key_points": "list of up to 5 key points",
            "topic": "one-word or short phrase topic label",
        },
    )


def classify_prompt(text: str, categories: List[str]) -> str:
    """Return a prompt that asks for text classification into given categories."""
    cats = " | ".join(f'"{c}"' for c in categories)
    return build_json_prompt(
        f'Classify the following text into one of the given categories:\n\n"{text}"',
        {
            "category": cats,
            "confidence": "number between 0.0 and 1.0",
            "reason": "one-sentence explanation",
        },
    )


# ─────────────────────────────────────────────────────────────
# Response formatter
# ─────────────────────────────────────────────────────────────

def format_structured_response(data: Dict) -> str:
    """Pretty-print a structured response dictionary."""
    lines = []
    for key, value in data.items():
        if isinstance(value, list):
            lines.append(f"📌 {key.replace('_', ' ').title()}:")
            for item in value:
                lines.append(f"   • {item}")
        else:
            lines.append(f"📌 {key.replace('_', ' ').title()}: {value}")
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────
# Quick demo
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Simulate model response
    fake_response = '''
    Sure! Here is the analysis:
    ```json
    {
      "sentiment": "positive",
      "confidence": 0.95,
      "emotions": ["joy", "satisfaction"],
      "reason": "The text uses enthusiastic and positive language."
    }
    ```
    '''

    print("🔍 Testing JSON extraction:")
    result = extract_json(fake_response)
    print(result)

    print("\n📊 Formatted output:")
    print(format_structured_response(result))

    print("\n📝 Sentiment analysis prompt sample:")
    prompt = sentiment_analysis_prompt("I absolutely love this new AI tool!")
    print(prompt)
