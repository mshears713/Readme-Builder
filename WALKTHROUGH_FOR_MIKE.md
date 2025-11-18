# Project Forge Walkthrough (For Mike)

## 1. Agent Roles (One-liners)
- **ConceptExpander** – cleans the raw idea and lists constraints.
- **GoalsAnalyzer** – turns the refined concept into learning + technical goals.
- **FrameworkSelector** – picks a friendly stack that matches the skill level.
- **PhaseDesigner** – lays out 5 phases with ~10 practical steps each.
- **TeacherAgent** – injects teaching_guidance into every step.
- **EvaluatorAgent** – scores the plan, checks structure, and flags issues.
- **PRDWriter** – converts the validated plan into a full README/PRD.

## 2. Architecture Snapshot
```
CLI / Streamlit / FastAPI input
        ↓
 Orchestration helpers (crew_config)
        ↓
 Agents run sequentially (Concept → Goals → Framework → Phases → Teacher → Evaluator → PRD)
        ↓
 Outputs land in dataclasses + README markdown
```

## 3. Pipeline Flow (happy path)
1. User supplies `raw_idea`, skill level, and phase target.
2. Phase 2 agents produce `ProjectIdea`, `ProjectGoals`, and `FrameworkChoice`.
3. PhaseDesigner + Teacher build a 5-phase plan with annotated steps.
4. Evaluator loops until rubric + structural checks pass.
5. PRDWriter turns the plan into markdown; UI/API/CLI store the files under `/output`.
6. Streamlit UI shows tabs for each agent, the FastAPI endpoint returns a preview, and the CLI prints a summary.

## 4. UI Overview
- **Home** – run the pipeline, see progress, review results.
- **Agent Tabs** – each agent has a dedicated page with context and logs.
- **Tracing Page** – displays LangSmith diagnostics and setup steps.
- **Logs Page** – captures stdout/stderr + structured events.

## 5. Directory Map (top-level)
- `project_forge/src/agents/` – one file per agent (creation + parsing helpers).
- `project_forge/src/models/` – dataclasses for ideas, goals, phases, plans.
- `project_forge/src/orchestration/` – CLI runner + crew wiring.
- `project_forge/src/api/` – FastAPI app for previews/full runs.
- `project_forge/src/utils/` – tracing setup, shared helpers.
- `streamlit_ui/` – Streamlit pages and UI utilities.
- `Dockerfile` + `docker/` – multi-stage container with entrypoint + healthcheck.

## 6. Data Movement
- CLI/UI/API all call the same orchestration helpers.
- Each agent writes plain text which gets parsed back into dataclasses (e.g., `ProjectPlan`).
- Streamlit stores intermediate objects in `st.session_state` so tabs stay in sync.
- Evaluator outputs an `EvaluationResult` with rubric scores, architecture notes, and recommendations.
- Final README plus metadata are saved to `/output/<project_name>_README.md`.

Keep things simple, focus on the one-line purpose of each piece, and treat this file as the map for future tweaks.
