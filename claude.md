# Project Forge — Claude Grounding Notes

## Purpose
- Transform a short CLI idea into a detailed teaching-style README/PRD.
- Keep outputs scoped to ~5 phases / 50 steps geared toward beginner/intermediate builders.
- Surfaces: CLI runner, Streamlit UI, FastAPI preview API, Docker image.

## Architecture Snapshot
```
CLI / Streamlit / FastAPI request
        ↓
project_forge.src.orchestration.crew_config (planning helpers)
        ↓
ConceptExpander → GoalsAnalyzer → FrameworkSelector → PhaseDesigner
        ↓
TeacherAgent → EvaluatorAgent → PRDWriter
        ↓
ProjectPlan dataclasses + README markdown persisted to /output
```
- CrewAI agents run sequentially so we can parse text outputs into dataclasses.
- Streamlit UI uses `streamlit_ui.utils` session helpers (`prepare_new_run_state`, `cleanup_asyncio_tasks`).
- FastAPI (`project_forge/src/api/app.py`) exposes `/healthz` + `/api/v1/plan` (dry-run preview + optional full pipeline).
- LangSmith diagnostics live in `project_forge/src/utils/tracing_setup.py` and are surfaced in CLI/UI/API.

## Agent Reference (inputs → outputs → purpose)
| Agent | Input | Output | One-line role |
| --- | --- | --- | --- |
| ConceptExpander | raw idea | `ProjectIdea` | Clean the idea, add constraints, capture vibe |
| GoalsAnalyzer | `ProjectIdea` | `ProjectGoals` | Split learning vs technical goals |
| FrameworkSelector | idea + goals + skill | `FrameworkChoice` | Suggest friendly stack & libraries |
| PhaseDesigner | idea + goals + stack | `Phase[]` | Build 5 phases × ~10 steps |
| TeacherAgent | plan | enriched `Step` data | Add `teaching_guidance` + learning arc |
| EvaluatorAgent | plan | `EvaluationResult` | Rubric scores, architecture notes, approval flag |
| PRDWriter | plan + eval | README markdown | Convert structured plan into narrative deliverable |

## Pipeline Logic
1. Inputs collected (idea, skill level, project type, time, max iterations).
2. Each agent runs through CrewAI tasks; outputs parsed into dataclasses defined in `project_models.py`.
3. Evaluator produces multi-paragraph critique with scores + resilience/testing feedback.
4. PRDWriter stitches everything into README/PRD and returns metadata (project name, readme text).
5. CLI writes file under `/output`, Streamlit renders per-agent tabs, FastAPI returns preview/full run payloads.

## Input / Output Models
- **Key models**: `ProjectIdea`, `ProjectGoals`, `FrameworkChoice`, `Phase`, `Step`, `ProjectPlan`, `EvaluationResult`.
- `Step` keeps `teaching_guidance` ↔ legacy `what_you_learn` in sync via `__setattr__` hook.
- Evaluator extends results with `architecture_notes`, `performance_alerts`, `resilience_risks`, `test_recommendations`, `naming_feedback`.
- API schemas live in `project_forge/src/api/app.py` (`PlanRequest`, `PlanPreview`, `PlanResponse`).
- LangSmith diagnostics surface via `collect_langsmith_diagnostics()` / `describe_langsmith_status()`.

## Ops & Tooling Notes
- `runner.py` is the single CLI entrypoint; it initializes tracing diagnostics, validates input, and routes to phase-specific helpers.
- Tests live in `project_forge/tests/` (API preview smoke test, tracing helpers, phase 5 structure smoke tests).
- Dockerfile is multi-stage, ARM-friendly, uses non-root `appuser`, with healthcheck hitting `/healthz`.
- Requirements pinned in both root and `project_forge/` subdir; FastAPI + Pydantic v2 + httpx + langsmith included.
- Streamlit UI resets state between runs to avoid zombie tasks; asynchronous cleanup uses `cleanup_asyncio_tasks()`.

Keep explanations simple and reference this file before modifying agents, API, or deployment surfaces.
