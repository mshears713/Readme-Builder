# Codebase Exploration Summary - Project Forge Agent Architecture

**Date**: November 17, 2025
**Project**: Project Forge - Multi-Agent README Generator
**Explored by**: Claude Code File Search Specialist

---

## Key Findings Overview

### 1. **What Agents Exist** ✓
The system contains **7 sequential agents**, each with a specific purpose:

1. **ConceptExpander** - Refines raw project ideas into structured concepts
2. **GoalsAnalyzer** - Extracts learning and technical goals
3. **FrameworkSelector** - Recommends technology stacks
4. **PhaseDesigner** - Creates 5-phase build plans (~50 steps)
5. **TeacherAgent** - Enriches steps with pedagogical annotations
6. **EvaluatorAgent** - Quality control and plan validation
7. **PRDWriterAgent** - Generates comprehensive README/PRD documents

**Total Agent Code**: 2,298 lines across 7 files

---

### 2. **Agent Implementation Locations** ✓
All agents are in: `/home/user/Readme-Builder/project_forge/src/agents/`

| File | Lines | Agent Name |
|------|-------|------------|
| concept_expander_agent.py | 219 | ConceptExpander |
| goals_analyzer_agent.py | 238 | GoalsAnalyzer |
| framework_selector_agent.py | 298 | FrameworkSelector |
| phase_designer_agent.py | 327 | PhaseDesigner |
| teacher_agent.py | 320 | TeacherAgent |
| evaluator_agent.py | 439 | EvaluatorAgent |
| prd_writer_agent.py | 452 | PRDWriterAgent |

---

### 3. **Agent Input/Output Structures** ✓
Well-defined data models in `/home/user/Readme-Builder/project_forge/src/models/project_models.py`:

**Data Models (6 core types):**
1. `ProjectIdea` - Raw description + refined summary + constraints
2. `ProjectGoals` - Learning goals + technical goals + priority notes
3. `FrameworkChoice` - Frontend/backend/storage/libraries selection
4. `Step` - Individual implementation task with dependencies
5. `Phase` - Group of ~10 steps with a theme
6. `ProjectPlan` - Complete plan with all above components

**Result Classes (3 pipeline results):**
- `PlanningResult` - Output from agents 1-3 (Phase 2)
- `FullPlanResult` - Output from agents 1-6 (Phase 3)
- `FullPlanWithReadmeResult` - Output from agents 1-7 (Phase 4)

**Data flows in sequence:**
```
Raw Text → ProjectIdea → ProjectGoals → FrameworkChoice 
→ List[Phase] → Enriched Phases → ProjectPlan → README Markdown
```

---

### 4. **How Reasoning is Captured** ✓

**Captured Through:**
1. **JSON Parsing** - Each agent outputs JSON that's parsed to data models
2. **Print Statements** - Visual progress indicators and decisions logged to console
3. **Rubric Scoring** - Evaluation creates detailed scores with feedback
4. **Consistency Reports** - Structural validation with error categories
5. **Teaching Annotations** - Every step includes "what you learn" explanations

**Key Capture Points:**
- Concept clarity scores
- Goal priorities and breakdowns
- Framework selection rationale
- Phase/step structure and dependencies
- Teaching value assessments
- Evaluation approval/rejection with feedback

---

### 5. **Logging Mechanisms** ✓

**CLI Logging** (in `runner.py`):
```python
logger = logging.getLogger("project_forge")
# Supports: DEBUG, INFO, WARNING, ERROR levels
# Can be controlled via --log-level and --verbose flags
```

**Configuration Logging** (`defaults.yaml`):
```yaml
logging:
  level: "INFO"
  log_agent_decisions: true
  log_intermediate_outputs: false
  save_intermediate_plans: false
```

**Print-Based Visibility:**
- Progress banners with "=" separators
- Status checkmarks (✓) for completed steps
- Numbered output from each agent
- Formatted tables and summaries
- Error messages with context

**Iteration Tracking:**
- Tracks how many refinement loops executed
- Maximum 2-3 iterations to prevent API cost overruns
- Provides feedback for each iteration

---

### 6. **Existing UI Components** ✓

**Current State**: **CLI-only, no web UI yet**

**What Exists:**
- Command-line interface in `runner.py` with argument parsing
- Text-based output formatting with visual indicators
- Configuration-driven defaults (`defaults.yaml`)
- Framework templates for different project types
- Skill level presets (beginner/intermediate/advanced)

**What Does NOT Exist:**
- Streamlit web interface
- Flask/Django application
- React frontend
- API server
- Database
- Web dashboard
- Visualization components

**Opportunity**: The Streamlit UI you're building can display:
- Live agent execution status
- Real-time progress tracking
- Intermediate agent outputs with detailed views
- Evaluation scores and feedback
- Plan visualization (phases, steps, dependencies)
- README preview with markdown rendering
- Execution history and plan comparison

---

## Architecture Strengths

1. **Clear Separation of Concerns**
   - Data models (project_models.py)
   - Agents (agent files)
   - Tools (rubric, consistency, text_cleaner)
   - Orchestration (crew_config.py, runner.py)

2. **Sequential Processing**
   - Each agent completes before next begins
   - Enables error checking and iteration loops
   - Clear data dependencies

3. **Structured Output**
   - JSON parsing with fallbacks
   - Type-safe Python dataclasses
   - Composition and chaining friendly

4. **Evaluation Loop**
   - Plans can be refined if they don't meet quality thresholds
   - Multi-criteria rubric scoring
   - Consistency validation

5. **Configuration-Driven**
   - Framework templates in YAML
   - Skill level presets
   - Project type configurations
   - Agent parameters customizable

---

## Files Generated for You

### 1. **AGENT_ARCHITECTURE_OVERVIEW.md** (1,219 lines)
Comprehensive architecture documentation including:
- Detailed agent descriptions
- Complete data model specifications
- Input/output contracts for each agent
- Data flow diagrams
- Reasoning capture mechanisms
- Logging configuration
- Tools reference
- Integration patterns
- UI recommendations

### 2. **STREAMLIT_UI_GUIDE.md** (380+ lines)
Practical implementation guide for Streamlit UI:
- Quick reference tables for agent outputs
- Import statements for all models
- Code examples for common UI patterns
- Session state recommendations
- Error handling patterns
- Performance optimization tips
- Testing strategies
- ASCII mockup of UI layout

### 3. **EXPLORATION_SUMMARY.md** (This file)
High-level overview of exploration findings

---

## Quick Start for Streamlit UI Development

### Essential Imports
```python
from project_forge.src.models.project_models import (
    ProjectIdea, ProjectGoals, FrameworkChoice, Phase, Step, ProjectPlan
)
from project_forge.src.orchestration.crew_config import (
    create_planning_crew, create_full_plan_crew, create_complete_pipeline
)
from project_forge.src.agents.evaluator_agent import EvaluationResult
from project_forge.src.tools.rubric_tool import RubricCriterion, RubricScore
```

### Main Entry Points
```python
# Phase 2: Planning (agents 1-3)
result = create_planning_crew(raw_idea, skill_level, verbose)

# Phase 3: Full Plan (agents 1-6)
result = create_full_plan_crew(raw_idea, skill_level, verbose, max_iterations)

# Phase 4: Complete Pipeline (agents 1-7)
result = create_complete_pipeline(raw_idea, skill_level, verbose, max_iterations)
```

### Key Data to Display
- **ProjectIdea**: refined_summary, constraints
- **ProjectGoals**: learning_goals[], technical_goals[], priority_notes
- **FrameworkChoice**: frontend, backend, storage, special_libs[]
- **Phase/Step**: index, name/title, description, what_you_learn, dependencies
- **EvaluationResult**: approved, scores{}, critical_issues[], suggestions[]

---

## Statistics

### Code Metrics
- **Agent Code**: 2,298 lines across 7 files
- **Orchestration**: 484 lines (crew_config.py) + 460 lines (runner.py)
- **Models**: 138 lines (project_models.py)
- **Tools**: ~400 lines (rubric_tool, consistency_tool, text_cleaner)
- **Total Project Forge Code**: ~4,000+ lines

### Agent Complexity
- Shortest agent: ConceptExpander (219 lines)
- Longest agent: PRDWriterAgent (452 lines)
- Average agent: 328 lines

### Data Model Density
- 6 core data classes
- 3 result wrapper classes
- All dataclass-based for type safety and serialization

### Configuration
- 170+ lines in defaults.yaml
- 5 skill level definitions
- 5 framework template definitions
- 3 project type definitions

---

## Key Architectural Decisions

1. **Sequential Not Parallel**: Agents run one after another, enabling error checking
2. **Structured Output**: LLM outputs parsed to Python dataclasses for type safety
3. **Evaluation Loop**: Plans refined iteratively until quality thresholds met
4. **Configuration-Driven**: Behavior customized via YAML, not code changes
5. **Teaching-First**: Pedagogical annotations integrated throughout pipeline
6. **CLI-Focused**: Current UI is command-line; web UI layer needed

---

## Recommendations for Streamlit UI

### Priority 1 (Must Have)
1. Display execution status (which agent, progress %)
2. Show agent outputs in tabs (concept, goals, framework, phases, etc.)
3. Display evaluation scores and approval status
4. Show README/PRD preview and export

### Priority 2 (Should Have)
1. Input form with skill level, project type dropdowns
2. Iteration tracking (showing refinement loops)
3. Error messages and critical issues display
4. Teaching annotations viewer for each step

### Priority 3 (Nice to Have)
1. Plan visualization (phase/step graph)
2. Execution history and plan comparison
3. Raw JSON viewer for debugging
4. Agent logs/reasoning output capture
5. Download as PDF option

---

## Testing Recommendations

1. **Unit Tests**: Test each agent in isolation
2. **Integration Tests**: Test full pipelines (Phase 2, 3, 4)
3. **Data Model Tests**: Serialization/deserialization roundtrips
4. **UI Tests**: Streamlit component rendering
5. **End-to-End Tests**: Full execution with real LLM

---

## Next Steps for Your Streamlit UI

1. **Review** the AGENT_ARCHITECTURE_OVERVIEW.md for complete details
2. **Read** STREAMLIT_UI_GUIDE.md for implementation patterns
3. **Start with** a simple single-agent demo (ConceptExpander)
4. **Build incrementally** adding one agent's UI at a time
5. **Use** the provided code examples for common patterns
6. **Test with** Phase 2 pipeline (simplest, only 3 agents)

---

## Resources Created

**File 1: AGENT_ARCHITECTURE_OVERVIEW.md**
- 1,219 lines
- Complete architectural reference
- Data model specifications
- Agent descriptions and contracts
- Data flow diagrams
- Logging and reasoning capture details

**File 2: STREAMLIT_UI_GUIDE.md** 
- 380+ lines
- Implementation guide
- Code examples
- Layout mockups
- Error handling patterns
- Performance tips

**File 3: EXPLORATION_SUMMARY.md** (This file)
- Executive summary
- Key findings
- Statistics
- Quick start guide
- Recommendations

---

## Contact Points

All exploration findings documented in:
- `/home/user/Readme-Builder/AGENT_ARCHITECTURE_OVERVIEW.md` 
- `/home/user/Readme-Builder/STREAMLIT_UI_GUIDE.md`
- `/home/user/Readme-Builder/EXPLORATION_SUMMARY.md` ← You are here

Source code locations:
- Agents: `/home/user/Readme-Builder/project_forge/src/agents/`
- Models: `/home/user/Readme-Builder/project_forge/src/models/project_models.py`
- Orchestration: `/home/user/Readme-Builder/project_forge/src/orchestration/`
- Tools: `/home/user/Readme-Builder/project_forge/src/tools/`
- CLI: `/home/user/Readme-Builder/project_forge/src/orchestration/runner.py`

---

**Exploration Complete** ✓

This codebase has a clean, well-structured multi-agent architecture ready for UI visualization. All necessary information has been documented for your Streamlit development.
