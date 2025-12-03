"""Utilities for parsing and repairing JSON from LLM responses."""

import json
import re
import logging

logger = logging.getLogger(__name__)


def extract_json(text: str) -> str:
    """Extract JSON from text that may contain markdown code blocks or other content."""
    if not text:
        return ""
    
    # Remove markdown code blocks
    text = text.replace("```json", "").replace("```", "").strip()
    
    # Find the JSON object or array
    # Try to find object first
    if "{" in text:
        start = text.find("{")
        # Find matching closing brace
        depth = 0
        for i, char in enumerate(text[start:], start):
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    return text[start:i+1]
    
    # Try to find array
    if "[" in text:
        start = text.find("[")
        depth = 0
        for i, char in enumerate(text[start:], start):
            if char == "[":
                depth += 1
            elif char == "]":
                depth -= 1
                if depth == 0:
                    return text[start:i+1]
    
    return text


def repair_json(json_str: str) -> str:
    """Attempt to repair common JSON errors from LLM responses."""
    if not json_str:
        return json_str
    
    original = json_str
    
    # Fix trailing commas before closing brackets/braces
    json_str = re.sub(r',\s*}', '}', json_str)
    json_str = re.sub(r',\s*]', ']', json_str)
    
    # Fix missing commas between elements (common LLM error)
    # Pattern: "value"\n  "key" -> "value",\n  "key"
    json_str = re.sub(r'"\s*\n\s*"', '",\n"', json_str)
    
    # Pattern: }\n  { -> },\n  {
    json_str = re.sub(r'}\s*\n\s*{', '},\n{', json_str)
    
    # Pattern: ]\n  [ -> ],\n  [
    json_str = re.sub(r']\s*\n\s*\[', '],\n[', json_str)
    
    # Fix unquoted keys (key: value -> "key": value)
    json_str = re.sub(r'([{,]\s*)([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'\1"\2":', json_str)
    
    # Fix single quotes to double quotes
    # Be careful not to replace single quotes inside strings
    # Simple approach: replace ' with " when it looks like a string delimiter
    json_str = re.sub(r"'([^']*)'", r'"\1"', json_str)
    
    # Remove any control characters that might have snuck in
    json_str = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', json_str)
    
    if json_str != original:
        logger.debug(f"JSON repaired: {len(original)} -> {len(json_str)} chars")
    
    return json_str


def safe_parse_json(text: str, default=None):
    """Safely parse JSON from LLM response with extraction and repair.
    
    Args:
        text: Raw text that may contain JSON
        default: Value to return if parsing fails (default: None)
    
    Returns:
        Parsed JSON object/array, or default if parsing fails
    """
    if not text:
        return default
    
    # Step 1: Extract JSON from text
    json_str = extract_json(text)
    
    if not json_str:
        logger.warning("No JSON found in text")
        return default
    
    # Step 2: Try parsing as-is
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.debug(f"Initial JSON parse failed: {e}")
    
    # Step 3: Try with repairs
    repaired = repair_json(json_str)
    try:
        return json.loads(repaired)
    except json.JSONDecodeError as e:
        logger.warning(f"JSON parse failed even after repair: {e}")
        logger.debug(f"Failed JSON (first 500 chars): {repaired[:500]}")
        return default


def safe_parse_json_with_error(text: str):
    """Parse JSON and return (result, error) tuple.
    
    Returns:
        Tuple of (parsed_json, None) on success, or (None, error_message) on failure
    """
    if not text:
        return None, "Empty text"
    
    json_str = extract_json(text)
    
    if not json_str:
        return None, "No JSON found in text"
    
    # Try parsing as-is
    try:
        return json.loads(json_str), None
    except json.JSONDecodeError as e:
        original_error = str(e)
    
    # Try with repairs
    repaired = repair_json(json_str)
    try:
        return json.loads(repaired), None
    except json.JSONDecodeError as e:
        return None, f"JSON parse failed: {original_error}"
