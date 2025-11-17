# Streamlit UI Implementation Guide for Project Forge

## Quick Reference: Data Models and Agent Outputs

### What You Need to Display in the UI

#### 1. **Execution Status & Progress**
```python
{
    "current_phase": int,           # 1=Planning, 2=Design, 3=Evaluation, 4=README
    "current_step": int,            # Within current phase (1-7 agents)
    "current_agent": str,           # "ConceptExpander" | "GoalsAnalyzer" | etc.
    "elapsed_time": float,          # seconds
    "estimated_total": float,       # estimated seconds
    "progress_percent": int,        # 0-100
}
```

#### 2. **Agent Outputs (in order of execution)**

| Agent | Output Model | Key Fields to Display |
|-------|---|---|
| **ConceptExpander** | `ProjectIdea` | `refined_summary`, `constraints` dict |
| **GoalsAnalyzer** | `ProjectGoals` | `learning_goals[]`, `technical_goals[]`, `priority_notes` |
| **FrameworkSelector** | `FrameworkChoice` | `frontend`, `backend`, `storage`, `special_libs[]` |
| **PhaseDesigner** | `List[Phase]` | Phase index, name, step count |
| **TeacherAgent** | Enriched phases | Each step's `what_you_learn` field |
| **EvaluatorAgent** | `EvaluationResult` | `approved` bool, `scores` dict, `feedback` str, `critical_issues[]` |
| **PRDWriter** | `str` | Raw markdown content |

#### 3. **Evaluation Scores**
```python
scores = {
    RubricCriterion.CLARITY: RubricScore(score=8, feedback="..."),
    RubricCriterion.FEASIBILITY: RubricScore(score=7, feedback="..."),
    RubricCriterion.TEACHING_VALUE: RubricScore(score=9, feedback="..."),
    RubricCriterion.TECHNICAL_DEPTH: RubricScore(score=8, feedback="..."),
    RubricCriterion.BALANCE: RubricScore(score=8, feedback="..."),
}
```

---

## File Locations to Import From

```python
# Data Models
from project_forge.src.models.project_models import (
    ProjectIdea, ProjectGoals, FrameworkChoice,
    Phase, Step, ProjectPlan
)

# Result Classes
from project_forge.src.orchestration.crew_config import (
    PlanningResult, FullPlanResult, FullPlanWithReadmeResult
)

# Evaluation
from project_forge.src.agents.evaluator_agent import EvaluationResult

# Rubric
from project_forge.src.tools.rubric_tool import (
    RubricCriterion, RubricScore, RubricEvaluation
)

# Orchestration Entry Points
from project_forge.src.orchestration.crew_config import (
    create_planning_crew,      # Phase 2
    create_full_plan_crew,     # Phase 3
    create_complete_pipeline   # Phase 4
)
```

---

## Agent Execution Pipeline

### Phase 2 (Planning Only)
```python
result: PlanningResult = create_planning_crew(
    raw_idea="Build a Streamlit app",
    skill_level="beginner",
    verbose=True
)

# Access outputs:
result.project_idea        # ProjectIdea
result.project_goals       # ProjectGoals
result.framework_choice    # FrameworkChoice
result.clarity_score       # RubricScore
```

### Phase 3 (Full Plan with Teaching)
```python
result: FullPlanResult = create_full_plan_crew(
    raw_idea="Build a Streamlit app",
    skill_level="beginner",
    verbose=True,
    max_iterations=2
)

# Access outputs:
result.project_plan        # ProjectPlan (all agents except PRDWriter)
result.evaluation          # EvaluationResult
result.iterations          # int (number of refinement loops)
```

### Phase 4 (Complete Pipeline with README)
```python
result: FullPlanWithReadmeResult = create_complete_pipeline(
    raw_idea="Build a Streamlit app",
    skill_level="beginner",
    verbose=True,
    max_iterations=2
)

# Access outputs:
result.project_plan        # ProjectPlan
result.evaluation          # EvaluationResult
result.readme_content      # str (markdown)
result.project_name        # str (generated name)
result.iterations          # int
```

---

## UI Layout Recommendation

```
┌─────────────────────────────────────────────────────────────┐
│ PROJECT FORGE - Streamlit Agent Execution UI                │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│ Input: [Text field for project idea] [Skill: Dropdown]      │
│        [Complexity: Dropdown] [Project Type: Dropdown]      │
│        [RUN PIPELINE] [PHASE: 2, 3, 4]                      │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│ EXECUTION STATUS                                             │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│ Phase: 2/4 | Agent: GoalsAnalyzer | Progress: 45% ████░    │
│ Elapsed: 23s | Estimated: 45s                               │
│ Status: Running...                                           │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│ AGENTS OUTPUT (Tabs)                                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│ [Concept] [Goals] [Framework] [Phases] [Teach] [Eval] [MD]  │
│                                                               │
│ ┌─────────────────────────────────────────────────────────┐  │
│ │ CONCEPT EXPANDER                                        │  │
│ ├─────────────────────────────────────────────────────────┤  │
│ │ Refined Summary:                                        │  │
│ │ "A web application that visualizes habit tracking..."   │  │
│ │                                                         │  │
│ │ Constraints:                                            │  │
│ │  • Time: 1-2 weeks                                      │  │
│ │  • Complexity: medium                                   │  │
│ │  • Skill Appropriateness: intermediate                  │  │
│ └─────────────────────────────────────────────────────────┘  │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│ EVALUATION RESULTS                                           │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│ Status: ✓ APPROVED                                           │
│                                                               │
│ Scores:                                                      │
│  • Clarity: 9/10 ████████░ "Crystal clear"                   │
│  • Feasibility: 8/10 ████████░ "Realistic scope"             │
│  • Teaching Value: 9/10 ████████░ "Excellent learning arc"   │
│  • Technical Depth: 8/10 ████████░ "Good complexity"         │
│  • Balance: 8/10 ████████░ "Even distribution"               │
│                                                               │
│ Iterations: 1/2                                              │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│ README PREVIEW (if completed)                                │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│ [Copy to Clipboard] [Download] [Full View]                  │
│ ┌─────────────────────────────────────────────────────────┐  │
│ │ # Habit Tracker Application                             │  │
│ │                                                         │  │
│ │ ## Overview                                             │  │
│ │ A Streamlit web application that helps users track...  │  │
│ │                                                         │  │
│ │ (First 50 lines of markdown)                            │  │
│ └─────────────────────────────────────────────────────────┘  │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Data Structures for UI State

```python
# Store this in Streamlit session state during execution
st.session_state.execution_state = {
    "started": bool,
    "completed": bool,
    "error": str or None,
    
    # Input params
    "raw_idea": str,
    "skill_level": str,
    "phase": int,  # 2, 3, or 4
    
    # Outputs by agent
    "planning_result": PlanningResult or None,
    "full_plan_result": FullPlanResult or None,
    "final_result": FullPlanWithReadmeResult or None,
    
    # Execution metadata
    "start_time": datetime,
    "elapsed_seconds": float,
    "current_agent": str,
    "progress_percent": int,
    
    # Display state
    "active_tab": str,  # which agent output to show
    "show_raw_json": bool,
}
```

---

## Common UI Patterns

### Displaying ProjectIdea
```python
st.subheader("Project Concept")
if plan.idea:
    st.write("**Refined Summary:**")
    st.write(plan.idea.refined_summary)
    
    st.write("**Constraints:**")
    cols = st.columns(2)
    for i, (key, value) in enumerate(plan.idea.constraints.items()):
        with cols[i % 2]:
            st.metric(key.title(), value)
```

### Displaying ProjectGoals
```python
st.subheader("Learning & Technical Goals")
col1, col2 = st.columns(2)

with col1:
    st.write("**Learning Goals:**")
    for i, goal in enumerate(plan.goals.learning_goals, 1):
        st.write(f"{i}. {goal}")

with col2:
    st.write("**Technical Goals:**")
    for i, goal in enumerate(plan.goals.technical_goals, 1):
        st.write(f"{i}. {goal}")

st.info(f"**Priority:** {plan.goals.priority_notes}")
```

### Displaying FrameworkChoice
```python
st.subheader("Technology Stack")
cols = st.columns(4)
with cols[0]:
    st.metric("Frontend", plan.framework.frontend or "None")
with cols[1]:
    st.metric("Backend", plan.framework.backend or "None")
with cols[2]:
    st.metric("Storage", plan.framework.storage or "None")
with cols[3]:
    if plan.framework.special_libs:
        st.write("**Libraries:**")
        st.write(", ".join(plan.framework.special_libs))
```

### Displaying Phases and Steps
```python
st.subheader("Project Structure")
for phase in plan.phases:
    with st.expander(f"Phase {phase.index}: {phase.name} ({len(phase.steps)} steps)"):
        st.write(phase.description)
        
        for step in phase.steps:
            st.write(f"**{step.index}. {step.title}**")
            st.write(f"*{step.description}*")
            if step.what_you_learn:
                st.info(f"📚 Learn: {step.what_you_learn}")
            if step.dependencies:
                st.caption(f"Depends on: Steps {', '.join(map(str, step.dependencies))}")
```

### Displaying Evaluation Scores
```python
st.subheader("Quality Evaluation")

if evaluation.approved:
    st.success("✓ Plan Approved!")
else:
    st.error("✗ Plan Needs Revision")

# Scores
cols = st.columns(len(evaluation.scores))
for col, (criterion, score) in zip(cols, evaluation.scores.items()):
    with col:
        st.metric(
            criterion.value.title(),
            f"{score.score}/10",
            delta=f"Pass" if score.passes() else "Fail"
        )
        st.caption(score.feedback)

# Issues
if evaluation.critical_issues:
    st.error("**Critical Issues:**")
    for issue in evaluation.critical_issues:
        st.write(f"• {issue}")

if evaluation.suggestions:
    st.warning("**Suggestions:**")
    for suggestion in evaluation.suggestions:
        st.write(f"• {suggestion}")
```

---

## Streaming Agent Output (Optional Enhancement)

For real-time progress display, you could capture CrewAI's verbose output:

```python
import io
import sys
from contextlib import redirect_stdout

# Capture agent output
captured_output = io.StringIO()
with redirect_stdout(captured_output):
    result = create_complete_pipeline(
        raw_idea=idea,
        skill_level=skill_level,
        verbose=True  # This writes to stdout
    )

agent_logs = captured_output.getvalue()

# Display in Streamlit
st.text_area("Agent Logs", agent_logs, height=200, disabled=True)
```

---

## Error Handling Patterns

```python
try:
    result = create_complete_pipeline(...)
    st.session_state.execution_state["completed"] = True
    
except ValueError as e:
    st.error(f"Validation Error: {e}")
    st.session_state.execution_state["error"] = str(e)
    
except KeyboardInterrupt:
    st.warning("Pipeline interrupted by user")
    
except Exception as e:
    st.error(f"Unexpected Error: {e}")
    st.session_state.execution_state["error"] = str(e)
    st.exception(e)  # Shows full traceback
```

---

## Performance Optimization Tips

1. **Cache Framework Config**: Load defaults.yaml once
   ```python
   @st.cache_resource
   def load_config():
       from project_forge.src.agents.framework_selector_agent import load_framework_config
       return load_framework_config()
   ```

2. **Store Results in Session State**: Avoid re-running pipeline
   ```python
   if "execution_state" not in st.session_state:
       st.session_state.execution_state = {...}
   ```

3. **Lazy Load Markdown Preview**: Only generate when tab selected
   ```python
   if markdown_tab.selected:
       with st.spinner("Rendering..."):
           st.markdown(final_result.readme_content)
   ```

4. **Limit Update Frequency**: Don't update UI faster than ~1Hz
   ```python
   import time
   last_update = time.time()
   if time.time() - last_update > 1.0:
       st.rerun()
       last_update = time.time()
   ```

---

## Testing the Integration

```python
# test_streamlit_ui.py
import pytest
from project_forge.src.orchestration.crew_config import create_planning_crew

def test_planning_crew():
    """Test that planning crew works end-to-end."""
    result = create_planning_crew(
        raw_idea="Build a simple CLI app",
        skill_level="beginner"
    )
    
    assert result.project_idea is not None
    assert result.project_goals is not None
    assert result.framework_choice is not None
    assert result.clarity_score is not None

def test_data_model_serialization():
    """Test that models can be serialized to JSON."""
    import json
    from dataclasses import asdict
    from project_forge.src.models.project_models import ProjectIdea
    
    idea = ProjectIdea(
        raw_description="Test",
        refined_summary="Test refined",
        constraints={"time": "1 week"}
    )
    
    # Should be serializable
    json_str = json.dumps(asdict(idea), default=str)
    assert "Test" in json_str
```

---

## Summary: What to Track in UI

1. **Input Parameters**: raw_idea, skill_level, phase, project_type
2. **Progress**: current_agent (1-7), elapsed_time, progress_percent
3. **Agent Outputs**: 7 result objects in sequence
4. **Evaluation**: scores dict, approval status, feedback, issues
5. **Final Output**: readme_content (markdown), project_name
6. **Metadata**: start_time, iterations, execution_errors

All of these map directly to the data structures defined in `/home/user/Readme-Builder/project_forge/src/models/project_models.py` and orchestrated in `/home/user/Readme-Builder/project_forge/src/orchestration/crew_config.py`.

