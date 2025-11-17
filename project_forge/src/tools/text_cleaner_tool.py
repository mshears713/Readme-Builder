"""
Text cleaning and normalization utilities for Project Forge.

These tools help ConceptExpanderAgent and other agents clean up raw user input,
remove noise, normalize whitespace, and prepare text for structured processing.
Used throughout the system to ensure consistent text quality.
"""

import re
from typing import List


def normalize_whitespace(text: str) -> str:
    """
    Normalize all whitespace in text to single spaces.

    Removes leading/trailing whitespace, collapses multiple spaces/tabs/newlines
    into single spaces, and ensures clean text flow.

    Args:
        text: Raw text with potentially messy whitespace

    Returns:
        Cleaned text with normalized spacing

    Example:
        >>> normalize_whitespace("Build   a\\n\\nStreamlit  app")
        'Build a Streamlit app'
    """
    # Replace all whitespace sequences (spaces, tabs, newlines) with single space
    cleaned = re.sub(r'\s+', ' ', text)
    return cleaned.strip()


def remove_filler_words(text: str) -> str:
    """
    Remove common filler words and phrases that add no semantic value.

    Helps clean up conversational input like "um, I want to maybe build..."
    into clearer statements for agent processing.

    Args:
        text: Text potentially containing filler words

    Returns:
        Text with filler words removed

    Example:
        >>> remove_filler_words("Um, I want to like build a dashboard, you know?")
        'I want to build a dashboard'
    """
    filler_patterns = [
        r'\b(um+|uh+|er+|ah+)\b',  # verbal fillers
        r'\b(like|you know|basically|actually)\b',  # conversational fillers
        r'\b(maybe|perhaps|sort of|kind of)\b',  # hedging words
    ]

    cleaned = text
    for pattern in filler_patterns:
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)

    # Clean up any resulting double spaces
    cleaned = normalize_whitespace(cleaned)
    return cleaned


def expand_common_abbreviations(text: str) -> str:
    """
    Expand common technical abbreviations to full words for clarity.

    Helps agents better understand user intent by spelling out common shorthand.

    Args:
        text: Text with potential abbreviations

    Returns:
        Text with abbreviations expanded

    Example:
        >>> expand_common_abbreviations("Build DB with REST API")
        'Build database with REST API'
    """
    abbreviations = {
        r'\bDB\b': 'database',
        r'\bAPI\b': 'API',  # Keep API as-is (too common)
        r'\bapp\b': 'application',
        r'\bconfig\b': 'configuration',
        r'\bauth\b': 'authentication',
    }

    expanded = text
    for abbrev, full in abbreviations.items():
        expanded = re.sub(abbrev, full, expanded, flags=re.IGNORECASE)

    return expanded


def clean_project_idea(raw_idea: str) -> str:
    """
    Apply full cleaning pipeline to a raw project idea.

    This is the main entry point used by ConceptExpanderAgent to prepare
    user input for structured processing. Combines all cleaning steps.

    Args:
        raw_idea: Raw string from CLI input

    Returns:
        Cleaned, normalized project idea ready for expansion

    Example:
        >>> clean_project_idea("Um, I want to  like build a DB  app\\n for tracking stuff")
        'I want to build a database application for tracking stuff'
    """
    cleaned = raw_idea
    cleaned = normalize_whitespace(cleaned)
    cleaned = remove_filler_words(cleaned)
    cleaned = expand_common_abbreviations(cleaned)
    cleaned = normalize_whitespace(cleaned)  # Final pass to clean up any artifacts
    return cleaned


def extract_keywords(text: str) -> List[str]:
    """
    Extract important keywords from project description.

    Identifies technical terms, frameworks, and key concepts that help
    agents understand the project domain and requirements.

    Args:
        text: Project description text

    Returns:
        List of extracted keywords (lowercase, deduplicated)

    Example:
        >>> extract_keywords("Build a Streamlit dashboard with async APIs")
        ['streamlit', 'dashboard', 'async', 'apis']
    """
    # Remove common stop words
    stop_words = {
        'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
        'i', 'want', 'need', 'build', 'create', 'make', 'develop'
    }

    # Tokenize and filter
    words = re.findall(r'\b\w+\b', text.lower())
    keywords = [w for w in words if w not in stop_words and len(w) > 2]

    # Return unique keywords in order of first appearance
    seen = set()
    unique_keywords = []
    for keyword in keywords:
        if keyword not in seen:
            seen.add(keyword)
            unique_keywords.append(keyword)

    return unique_keywords
