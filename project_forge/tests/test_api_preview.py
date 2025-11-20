"""Smoke tests for the FastAPI preview endpoint."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

pytest.importorskip("fastapi")
from fastapi.testclient import TestClient  # noqa: E402

from src.api.app import app


def test_plan_preview_endpoint():
    client = TestClient(app)
    response = client.post(
        "/api/v1/plan",
        json={
            "idea": "Build a calm vibe coding dashboard that tracks habits",
            "dry_run": True,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["preview"]["clarity_score"] >= 0
    status = data["preview"]["langsmith_status"]
    allowed = {"ready", "disabled", "missing_api_key", "pending"}
    assert status in allowed or status.startswith("error")
    assert data["ran_pipeline"] is False
