"""FastAPI application that exposes a lightweight Project Forge API."""

from __future__ import annotations

import os
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from ..tools.rubric_tool import evaluate_concept_clarity
from ..utils.tracing_setup import collect_langsmith_diagnostics

try:
    # Crew imports are optional so we can still serve preview endpoints without an API key.
    from ..orchestration.crew_config import create_complete_pipeline
except Exception:  # pragma: no cover - optional dependency during tests
    create_complete_pipeline = None


app = FastAPI(
    title="Project Forge API",
    version="1.0.0",
    summary="Preview or execute the Project Forge planning pipeline via HTTP.",
)


class PlanRequest(BaseModel):
    """Request model for pipeline preview/execution."""

    idea: str = Field(..., min_length=10, description="Raw project idea text")
    skill_level: str = Field(
        "intermediate",
        pattern="^(beginner|intermediate|advanced)$",
        description="Skill level presets used throughout the pipeline",
    )
    phase: int = Field(4, ge=2, le=4, description="Which pipeline phase to execute")
    project_type: str = Field("medium", description="Scope preset (toy/medium/ambitious)")
    time_constraint: str = Field("1-2 weeks", description="Timeline for evaluator context")
    dry_run: bool = Field(True, description="When True, run heuristics only and skip LLM calls")


class PlanPreview(BaseModel):
    """Small preview of what the pipeline would generate."""

    summary: str
    clarity_score: int
    clarity_feedback: str
    estimated_steps: int
    recommended_phases: int
    warnings: List[str]
    langsmith_status: str


class PlanResponse(BaseModel):
    """Response payload for the /plan endpoint."""

    preview: PlanPreview
    ran_pipeline: bool
    project_name: Optional[str] = None
    evaluation_feedback: Optional[str] = None
    readme_excerpt: Optional[str] = None


@app.get("/healthz")
async def healthcheck() -> dict:
    """Simple health endpoint used by Docker healthchecks."""

    return {
        "status": "ok",
        "app_mode": os.getenv("APP_MODE", "streamlit"),
    }


def _build_preview_payload(payload: PlanRequest) -> PlanPreview:
    """Generate a heuristic preview without hitting LLM providers."""

    clarity = evaluate_concept_clarity(payload.idea)
    warnings: List[str] = []
    if clarity.score < clarity.pass_threshold:
        warnings.append("Concept clarity is low; consider refining the idea text before running agents.")

    estimated_steps = max(25, min(60, clarity.score * 5))
    langsmith_status = collect_langsmith_diagnostics().status_label

    return PlanPreview(
        summary=payload.idea.strip(),
        clarity_score=clarity.score,
        clarity_feedback=clarity.feedback,
        estimated_steps=estimated_steps,
        recommended_phases=5,
        warnings=warnings,
        langsmith_status=langsmith_status,
    )


@app.post("/api/v1/plan", response_model=PlanResponse)
async def plan_endpoint(payload: PlanRequest) -> PlanResponse:
    """Preview the plan or run the full pipeline if configured."""

    preview = _build_preview_payload(payload)
    openai_key = os.getenv("OPENAI_API_KEY")

    if payload.dry_run or not openai_key or create_complete_pipeline is None:
        if not openai_key and not payload.dry_run:
            preview.warnings.append("OPENAI_API_KEY missing; returned preview instead of executing agents.")
        return PlanResponse(preview=preview, ran_pipeline=False)

    try:
        result = create_complete_pipeline(
            raw_idea=payload.idea,
            skill_level=payload.skill_level,
            verbose=False,
            max_iterations=2,
        )
    except Exception as exc:  # pragma: no cover - network dependent
        raise HTTPException(status_code=500, detail=f"Pipeline execution failed: {exc}") from exc

    excerpt = (result.readme_content or "").split("\n")[:40]
    preview_summary = "\n".join(excerpt)

    return PlanResponse(
        preview=preview,
        ran_pipeline=True,
        project_name=getattr(result, "project_name", None),
        evaluation_feedback=getattr(result.evaluation, "feedback", None),
        readme_excerpt=preview_summary,
    )
