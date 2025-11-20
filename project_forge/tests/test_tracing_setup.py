"""Unit tests for tracing diagnostics helpers."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.tracing_setup import (
    LangSmithDiagnostics,
    collect_langsmith_diagnostics,
    describe_langsmith_status,
    get_tracing_info,
)


def test_collect_langsmith_diagnostics_defaults(monkeypatch):
    monkeypatch.delenv("LANGCHAIN_TRACING_V2", raising=False)
    monkeypatch.delenv("LANGCHAIN_API_KEY", raising=False)

    diag = collect_langsmith_diagnostics()
    assert diag.enabled_flag is False
    assert diag.status_label == "disabled"


def test_get_tracing_info_structure(monkeypatch):
    monkeypatch.setenv("LANGCHAIN_TRACING_V2", "true")
    monkeypatch.setenv("LANGCHAIN_API_KEY", "test-key")

    info = get_tracing_info()
    assert "langsmith" in info
    assert "langfuse" in info
    assert info["langsmith"]["has_api_key"] is True


def test_describe_langsmith_status_handles_error():
    diag = LangSmithDiagnostics(
        enabled_flag=True,
        api_key_present=True,
        project_name="project-forge",
        endpoint="https://api.smith.langchain.com",
    )
    diag.error_message = "network timeout"

    summary = describe_langsmith_status(diag)

    assert "LangSmith status" in summary
    assert "network timeout" in summary
