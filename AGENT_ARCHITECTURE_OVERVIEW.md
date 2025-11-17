# Project Forge - Comprehensive Agent Architecture Overview

## Executive Summary

Project Forge is a multi-agent system using **CrewAI** that transforms raw project ideas into comprehensive README/PRD documents ready for code LLMs. The system contains **7 specialized agents** that work sequentially, each with distinct inputs/outputs and well-defined responsibilities.

**Key Stats:**
- 2,298 lines of agent code across 7 agent files
- 6 supporting data models (ProjectIdea, ProjectGoals, FrameworkChoice, Phase, Step, ProjectPlan)
- 3 tool modules (rubric, consistency, text_cleaner)
- CLI entrypoint with logging infrastructure
- Configuration-driven design with defaults.yaml

---

## 1. AGENTS THAT EXIST IN THIS PROJECT

### Overview Table

| # | Agent Name | File | Lines | Role | Input | Output |
|---|---|---|---|---|---|---|
| 1 | ConceptExpander | `concept_expander_agent.py` | 219 | Transforms raw ideas into structured concepts | Raw user text | ProjectIdea |
| 2 | GoalsAnalyzer | `goals_analyzer_agent.py` | 238 | Extracts learning & technical goals | ProjectIdea | ProjectGoals |
| 3 | FrameworkSelector | `framework_selector_agent.py` | 298 | Recommends tech stacks | ProjectIdea + ProjectGoals | FrameworkChoice |
| 4 | PhaseDesigner | `phase_designer_agent.py` | 327 | Creates 5-phase build plans with ~50 steps | All above + skill level | List[Phase] |
| 5 | TeacherAgent | `teacher_agent.py` | 320 | Enriches steps with pedagogical annotations | Phases + ProjectGoals | Enriched Phases + teaching notes |
| 6 | EvaluatorAgent | `evaluator_agent.py` | 439 | Quality control & validation | ProjectPlan | EvaluationResult |
| 7 | PRDWriterAgent | `prd_writer_agent.py` | 452 | Converts plan to markdown README | ProjectPlan | README/PRD markdown |

### Detailed Agent Descriptions

#### 1. ConceptExpander Agent
**Location:** `/home/user/Readme-Builder/project_forge/src/agents/concept_expander_agent.py`

**Purpose:** Transform vague, messy user input into a structured, clear project concept.

**Key Functions:**
- `create_concept_expander_agent()` - Creates the CrewAI Agent
- `create_concept_expansion_task()` - Defines the task with prompts
- `parse_concept_expansion_result()` - Parses JSON output to ProjectIdea
- `expand_concept()` - High-level entry point

**Responsibilities:**
- Clean and normalize raw text
- Identify implicit constraints (time, complexity, scope)
- Expand vague ideas into concrete concepts
- Remove ambiguity while preserving intent

**Agent Personality:** Expert product strategist and technical architect

---

#### 2. GoalsAnalyzer Agent
**Location:** `/home/user/Readme-Builder/project_forge/src/agents/goals_analyzer_agent.py`

**Purpose:** Extract clear learning objectives and technical deliverables from project concepts.

**Key Functions:**
- `create_goals_analyzer_agent()` - Creates the agent
- `create_goals_analysis_task()` - Defines the task
- `parse_goals_analysis_result()` - Parses JSON to ProjectGoals
- `analyze_goals()` - Entry point

**Responsibilities:**
- Identify learning objectives (concepts, skills, patterns)
- Identify technical deliverables (features, components, capabilities)
- Prioritize goals based on project focus
- Ensure goals are specific, measurable, achievable

**Agent Personality:** Skilled educator AND technical architect

---

#### 3. FrameworkSelector Agent
**Location:** `/home/user/Readme-Builder/project_forge/src/agents/framework_selector_agent.py`

**Purpose:** Recommend appropriate technology stacks based on project and skill level.

**Key Functions:**
- `create_framework_selector_agent()` - Creates the agent
- `create_framework_selection_task()` - Defines the task
- `parse_framework_selection_result()` - Parses JSON to FrameworkChoice
- `load_framework_config()` - Loads defaults.yaml templates
- `select_frameworks()` - Entry point

**Responsibilities:**
- Choose frontend frameworks (Streamlit, React, Flask, CLI-only)
- Choose backend frameworks (FastAPI, Flask, Django, scripts)
- Choose storage solutions (SQLite, PostgreSQL, JSON, etc.)
- Select domain-specific libraries (CrewAI, LangChain, BeautifulSoup, etc.)
- Balance simplicity, learning value, and project needs

**Agent Personality:** Pragmatic tech lead with deep framework expertise

---

#### 4. PhaseDesigner Agent
**Location:** `/home/user/Readme-Builder/project_forge/src/agents/phase_designer_agent.py`

**Purpose:** Break projects into 5 logical phases with ~10 concrete, actionable steps each.

**Key Functions:**
- `create_phase_designer_agent()` - Creates the agent
- `create_phase_design_task()` - Defines the task with strict structure guidelines
- `parse_phase_design_result()` - Parses JSON to List[Phase]
- (Also handles step dependency parsing)

**Responsibilities:**
- Create 5 phases with ~50 total steps
- Ensure each step is 30-90 minutes of work
- Make steps concrete with tangible deliverables
- Maintain proper dependencies between steps
- Keep scope realistic and achievable

**Agent Personality:** Expert project architect and engineering manager

---

#### 5. TeacherAgent Agent
**Location:** `/home/user/Readme-Builder/project_forge/src/agents/teacher_agent.py`

**Purpose:** Enrich project plans with pedagogical annotations explaining learning value.

**Key Functions:**
- `create_teacher_agent()` - Creates the agent
- `create_teaching_enrichment_task()` - Defines the task
- `parse_teaching_enrichment_result()` - Parses JSON, enriches Phases
- (No separate entry point function)

**Responsibilities:**
- Add "what_you_learn" annotations to every step
- Explain concepts, patterns, and skills each step teaches
- Create cohesive learning narrative across all phases
- Ensure progressive skill building
- Make pedagogical value explicit and clear

**Agent Personality:** Expert technical educator and learning designer

---

#### 6. EvaluatorAgent Agent
**Location:** `/home/user/Readme-Builder/project_forge/src/agents/evaluator_agent.py`

**Purpose:** Quality control and validation of project plans against rubrics.

**Key Functions:**
- `create_evaluator_agent()` - Creates the agent
- `evaluate_plan_quality()` - Heuristic evaluation using rubrics
- `create_plan_evaluation_task()` - Defines LLM-based evaluation task
- `evaluate_project_plan()` - Main entry point combining both evaluation methods

**Responsibilities:**
- Evaluate plan quality using rubrics (clarity, feasibility, teaching value, balance, technical depth)
- Run consistency checks (phase counts, step numbering, dependencies)
- Decide whether to approve or request refinements
- Provide specific, actionable feedback
- Support multiple evaluation modes

**Agent Personality:** Expert technical reviewer and QA specialist

**Special Outputs:**
- Returns `EvaluationResult` with scores, consistency report, feedback, critical issues, and suggestions

---

#### 7. PRDWriterAgent Agent
**Location:** `/home/user/Readme-Builder/project_forge/src/agents/prd_writer_agent.py`

**Purpose:** Convert structured ProjectPlan data into comprehensive, narrative README/PRD documents.

**Key Functions:**
- `create_prd_writer_agent()` - Creates the agent
- `create_prd_writing_task()` - Defines the task with template structure
- `parse_prd_writing_result()` - Extracts markdown from LLM output
- `generate_project_name()` - Creates names from ProjectPlan

**Responsibilities:**
- Convert structured data into clear narrative documentation
- Embed teaching notes and learning objectives throughout
- Create standardized README structure
- Include all technical details needed for implementation
- Make document actionable for code LLMs

**Agent Personality:** World-class technical documentation specialist

---

## 2. AGENT IMPLEMENTATIONS LOCATION MAP

### Directory Structure

```
/home/user/Readme-Builder/project_forge/src/agents/
├── __init__.py                      (5 lines - imports)
├── concept_expander_agent.py         (219 lines)
├── goals_analyzer_agent.py           (238 lines)
├── framework_selector_agent.py       (298 lines)
├── phase_designer_agent.py           (327 lines)
├── teacher_agent.py                  (320 lines)
├── evaluator_agent.py                (439 lines)
└── prd_writer_agent.py               (452 lines)
    Total: 2,298 lines
```

### File Locations (Absolute Paths)

```
/home/user/Readme-Builder/project_forge/src/agents/concept_expander_agent.py
/home/user/Readme-Builder/project_forge/src/agents/goals_analyzer_agent.py
/home/user/Readme-Builder/project_forge/src/agents/framework_selector_agent.py
/home/user/Readme-Builder/project_forge/src/agents/phase_designer_agent.py
/home/user/Readme-Builder/project_forge/src/agents/teacher_agent.py
/home/user/Readme-Builder/project_forge/src/agents/evaluator_agent.py
/home/user/Readme-Builder/project_forge/src/agents/prd_writer_agent.py
```

### Orchestration Files

```
/home/user/Readme-Builder/project_forge/src/orchestration/crew_config.py (484 lines)
  - Defines PlanningResult, FullPlanResult, FullPlanWithReadmeResult data classes
  - create_planning_crew() - Phase 2 pipeline (agents 1-3)
  - create_full_plan_crew() - Phase 3 pipeline (agents 1-6)
  - create_complete_pipeline() - Phase 4 pipeline (agents 1-7)

/home/user/Readme-Builder/project_forge/src/orchestration/runner.py (460 lines)
  - CLI entrypoint with argument parsing
  - Logging setup and configuration
  - Error handling and user feedback
  - File output for Phase 4
```

---

## 3. STRUCTURE OF AGENT INPUTS AND OUTPUTS

### Data Model Architecture

**Location:** `/home/user/Readme-Builder/project_forge/src/models/project_models.py`

All data flows through these structured models:

### 3.1 ProjectIdea

```python
@dataclass
class ProjectIdea:
    """Raw and refined project concept with constraints."""
    raw_description: str              # Original user input
    refined_summary: str              # Cleaned, expanded version
    constraints: Dict[str, Any]       # time, complexity, hardware, etc.

# Example:
ProjectIdea(
    raw_description="Build a Streamlit app",
    refined_summary="A Streamlit web application for habit tracking with SQLite persistence...",
    constraints={
        "time": "1-2 weeks",
        "complexity": "medium",
        "scope": "...",
        "technical_requirements": "...",
        "skill_appropriateness": "intermediate"
    }
)
```

**Input to:** ProjectIdea (ConceptExpander receives raw_description)
**Output from:** ConceptExpanderAgent
**Used by:** GoalsAnalyzer, FrameworkSelector, PhaseDesigner

---

### 3.2 ProjectGoals

```python
@dataclass
class ProjectGoals:
    """Learning and technical objectives."""
    learning_goals: List[str]         # e.g., ["async/await patterns", "API design"]
    technical_goals: List[str]        # e.g., ["REST API", "web scraper"]
    priority_notes: str               # Which goals are most important

# Example:
ProjectGoals(
    learning_goals=[
        "Understand async/await for concurrent API calls",
        "Practice component-based UI architecture",
        "Learn database schema design"
    ],
    technical_goals=[
        "Build a web scraper with async requests",
        "Create an interactive dashboard",
        "Implement user authentication"
    ],
    priority_notes="Focus on core features; auth is nice-to-have"
)
```

**Input to:** GoalsAnalyzer (receives ProjectIdea)
**Output from:** GoalsAnalyzerAgent
**Used by:** FrameworkSelector, PhaseDesigner, TeacherAgent, PRDWriter

---

### 3.3 FrameworkChoice

```python
@dataclass
class FrameworkChoice:
    """Technology stack recommendations."""
    frontend: Optional[str]           # e.g., "Streamlit", "React", None
    backend: Optional[str]            # e.g., "FastAPI", "Flask", "CLI-only"
    storage: Optional[str]            # e.g., "SQLite", "PostgreSQL"
    special_libs: List[str]           # e.g., ["CrewAI", "LangChain", "BeautifulSoup"]

# Example:
FrameworkChoice(
    frontend="Streamlit",
    backend="FastAPI",
    storage="PostgreSQL",
    special_libs=["pandas", "sqlalchemy", "plotly"]
)
```

**Input to:** FrameworkSelector (receives ProjectIdea + ProjectGoals)
**Output from:** FrameworkSelectorAgent
**Used by:** PhaseDesigner, PRDWriter

---

### 3.4 Step

```python
@dataclass
class Step:
    """Single implementation step within a phase."""
    index: int                        # Global step number (1-50)
    title: str                        # e.g., "Create user authentication endpoint"
    description: str                  # Detailed instructions
    what_you_learn: str               # Teaching annotation (added by TeacherAgent)
    dependencies: List[int]           # Prerequisite step indices

# Example:
Step(
    index=15,
    title="Implement user registration endpoint",
    description="Create a POST /users endpoint that validates input, hashes passwords, and stores in DB...",
    what_you_learn="Learn request validation patterns and password security best practices...",
    dependencies=[12, 13, 14]
)
```

**Input to:** TeacherAgent (receives Steps from PhaseDesigner)
**Output from:** PhaseDesignerAgent
**Modified by:** TeacherAgent (adds what_you_learn field)
**Used by:** EvaluatorAgent, PRDWriter

---

### 3.5 Phase

```python
@dataclass
class Phase:
    """Major milestone containing multiple steps."""
    index: int                        # Phase number (1-5)
    name: str                         # e.g., "Foundations & Models"
    description: str                  # What this phase accomplishes
    steps: List[Step]                 # ~10 steps per phase

# Example:
Phase(
    index=1,
    name="Foundations & Models",
    description="Set up project structure, define core data models, and establish the foundation...",
    steps=[
        Step(1, "Create project structure", ...),
        Step(2, "Define database models", ...),
        # ... ~8 more steps
    ]
)
```

**Input to:** TeacherAgent (receives Phases from PhaseDesigner)
**Output from:** PhaseDesignerAgent
**Modified by:** TeacherAgent (enriches steps)
**Used by:** EvaluatorAgent, PRDWriter

---

### 3.6 ProjectPlan

```python
@dataclass
class ProjectPlan:
    """Complete project plan with all components."""
    idea: ProjectIdea                 # Refined concept
    goals: ProjectGoals               # Learning & technical objectives
    framework: FrameworkChoice        # Technology stack
    phases: List[Phase]               # 5 phases with ~50 steps
    teaching_notes: str               # Global pedagogical commentary

# Example:
ProjectPlan(
    idea=ProjectIdea(...),
    goals=ProjectGoals(...),
    framework=FrameworkChoice(...),
    phases=[Phase(...), Phase(...), ...],  # 5 phases
    teaching_notes="This project teaches modern web development..."
)
```

**Input to:** EvaluatorAgent, PRDWriter
**Output from:** Assembled by crew_config.py after TeacherAgent enrichment
**Final destination:** README/PRD generation

---

### 3.7 Supporting Result Classes

#### PlanningResult (Phase 2)
```python
@dataclass
class PlanningResult:
    project_idea: ProjectIdea
    project_goals: ProjectGoals
    framework_choice: FrameworkChoice
    clarity_score: Optional[Any] = None
```

#### FullPlanResult (Phase 3)
```python
@dataclass
class FullPlanResult:
    project_plan: ProjectPlan
    evaluation: EvaluationResult
    iterations: int = 1
```

#### FullPlanWithReadmeResult (Phase 4)
```python
@dataclass
class FullPlanWithReadmeResult:
    project_plan: ProjectPlan
    evaluation: EvaluationResult
    readme_content: str
    project_name: str
    iterations: int = 1
```

#### EvaluationResult (from EvaluatorAgent)
```python
@dataclass
class EvaluationResult:
    approved: bool
    scores: Dict[RubricCriterion, RubricScore]
    consistency_report: Optional[ConsistencyReport]
    feedback: str
    critical_issues: List[str]
    suggestions: List[str]
```

---

### 3.8 Data Flow Diagram

```
Raw Idea Text (from CLI)
    ↓
ConceptExpander → ProjectIdea
    ↓
GoalsAnalyzer → ProjectGoals
    ↓
FrameworkSelector → FrameworkChoice
    ↓
PhaseDesigner → List[Phase] with Step objects
    ↓
TeacherAgent → Enriched Phases (with what_you_learn)
    ↓
EvaluatorAgent → EvaluationResult (approval, scores, feedback)
    ↓ (if approved)
ProjectPlan = (idea + goals + framework + phases + teaching_notes)
    ↓
PRDWriter → README/PRD Markdown
    ↓
Output File (*.md)
```

---

## 4. HOW REASONING IS CAPTURED AND LOGGED

### 4.1 Agent Reasoning Output Capture

Each agent's reasoning is captured through:

**1. CrewAI Task Execution:**
```python
# Each task execution produces text output from the LLM
result = task.execute()  # Returns string of agent's reasoning
```

**2. Structured Parsing:**
Each agent has a `parse_*_result()` function that:
- Extracts JSON from LLM output
- Handles markdown code blocks
- Provides fallbacks for parsing errors
- Returns structured data models

**Example from concept_expander_agent.py:**
```python
def parse_concept_expansion_result(result: str, raw_idea: str) -> ProjectIdea:
    """Parse agent's JSON output into ProjectIdea object."""
    try:
        # Handle markdown code blocks
        if clean_result.startswith("```"):
            lines = clean_result.split("\n")
            clean_result = "\n".join(lines[1:-1])
        
        data = json.loads(clean_result)
        
        return ProjectIdea(
            raw_description=raw_idea,
            refined_summary=data.get("refined_summary", raw_idea),
            constraints=data.get("constraints", {})
        )
    except (json.JSONDecodeError, KeyError, AttributeError) as e:
        print(f"Warning: Could not parse agent output as JSON: {e}")
        # Fallback to raw output
        return ProjectIdea(
            raw_description=raw_idea,
            refined_summary=result.strip(),
            constraints={"parsing_error": str(e)}
        )
```

**3. Print-Based Visibility:**
Throughout the pipeline, key decisions are printed:

```python
# From crew_config.py - create_planning_crew()
print("STEP 1/3: Expanding project concept...")
print(f"Raw idea: {raw_idea}\n")

concept_result = concept_task.execute()
project_idea = parse_concept_expansion_result(concept_result, raw_idea)

print(f"✓ Refined concept:")
print(f"  {project_idea.refined_summary}\n")
print(f"  Constraints: {project_idea.constraints}\n")

clarity_score = evaluate_concept_clarity(project_idea.refined_summary)
print(f"  Clarity score: {clarity_score.score}/10")
print(f"  Feedback: {clarity_score.feedback}\n")
```

### 4.2 Intermediate Outputs Display

The pipeline displays intermediate results at each stage:

**Phase 2 Output (Planning):**
```
PLANNING CREW - Phase 2
========================

STEP 1/3: Expanding project concept...
✓ Refined concept:
  {refined summary}
  Constraints: {constraints}
  Clarity score: 8/10

STEP 2/3: Analyzing learning and technical goals...
✓ Learning goals:
  - {goal 1}
  - {goal 2}
  ...

STEP 3/3: Selecting technology stack...
✓ Selected frameworks:
  Frontend: Streamlit
  Backend: FastAPI
  Storage: PostgreSQL
  Libraries: pandas, sqlalchemy, plotly
```

**Phase 3 Output (Full Plan):**
```
FULL PLAN CREW - Phase 3
========================

STEP 4: Designing project phases and steps...
✓ Created 5 phases with 50 total steps

STEP 5: Adding teaching annotations to steps...
✓ Added teaching annotations to 48/50 steps

STEP 6: Evaluating plan quality...
✓ Plan approved after 1 iteration(s)!
```

### 4.3 Rubric Scores and Feedback

The EvaluatorAgent returns detailed scoring:

```python
@dataclass
class RubricScore:
    criterion: RubricCriterion
    score: int                  # 0-10
    feedback: str               # Explanation of score
    pass_threshold: int = 7

# Criteria evaluated:
- CLARITY (how clear is the concept/plan?)
- FEASIBILITY (is it realistic to complete?)
- TEACHING_VALUE (does it teach valuable skills?)
- TECHNICAL_DEPTH (appropriate complexity level?)
- COMPLETENESS (all required parts present?)
- BALANCE (phases/steps evenly distributed?)
```

**Evaluation feedback example:**
```
Plan approved! ✓

Scores:
- Clarity: 9/10
- Feasibility: 8/10
- Teaching Value: 9/10
- Technical Depth: 8/10
- Balance: 8/10

Structure: 50 steps across 5 phases
Project Type: medium (1-2 weeks)
```

### 4.4 Consistency Checking

The EvaluatorAgent performs structural validation:

```python
@dataclass
class ConsistencyIssue:
    severity: str              # 'error' or 'warning'
    category: str              # e.g., 'phase_count', 'step_numbering'
    message: str
    location: str              # e.g., 'Phase 2, Step 5'

@dataclass
class ConsistencyReport:
    issues: List[ConsistencyIssue]
    passed: bool
    summary: str
    
    def has_errors(self) -> bool
    def has_warnings(self) -> bool
    def get_error_count(self) -> int
    def get_warning_count(self) -> int
```

---

## 5. LOGGING MECHANISMS IN PLACE

### 5.1 CLI Logging Configuration

**Location:** `/home/user/Readme-Builder/project_forge/src/orchestration/runner.py`

```python
def setup_logging(log_level: str, verbose: bool) -> logging.Logger:
    """
    Configure logging for Project Forge pipeline.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        verbose: Whether to enable verbose output
    
    Returns:
        Configured logger instance
    """
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    logger = logging.getLogger("project_forge")
    
    if verbose:
        logger.setLevel(logging.DEBUG)
    
    return logger
```

**CLI Arguments for Logging:**
```
--verbose              Enable verbose output (DEBUG level)
--log-level {DEBUG,INFO,WARNING,ERROR}
                      Set logging level (default: INFO)
```

### 5.2 Logging Points in Pipeline

**In runner.py main():**
```python
logger = setup_logging(args.log_level, args.verbose)

# Logging throughout execution
logger.info("Project Forge starting...")
logger.info(f"Running Phase {args.phase} with skill level: {args.skill}")
logger.debug(f"Full idea text: {idea}")

logger.info("Starting Phase 2: Planning crew")
logger.debug("Creating planning crew agents...")
logger.info("Phase 2 planning crew completed successfully")

logger.info("Starting Phase 4: Complete pipeline with README generation")
start_time = datetime.now()
result = create_complete_pipeline(...)
elapsed_time = (datetime.now() - start_time).total_seconds()
logger.info(f"Complete pipeline finished in {elapsed_time:.2f} seconds")

logger.info(f"Writing README to: {output_path}")
logger.info(f"README written successfully ({len(result.readme_content)} characters)")
```

**Error Logging:**
```python
except ValueError as e:
    logger.error(f"Validation error: {e}")
except FileNotFoundError as e:
    logger.error(f"File not found: {e}")
except PermissionError as e:
    logger.error(f"Permission error: {e}")
except Exception as e:
    logger.error(f"Unexpected error: {e}", exc_info=True)
```

### 5.3 Configuration-Based Logging

**Location:** `/home/user/Readme-Builder/project_forge/src/config/defaults.yaml`

```yaml
# Logging and Debug
logging:
  level: "INFO"  # DEBUG, INFO, WARNING, ERROR
  log_agent_decisions: true
  log_intermediate_outputs: false
  save_intermediate_plans: false
```

### 5.4 Print-Based Visibility (Human-Readable Output)

The system uses extensive print statements for CLI feedback:

```python
# Banner outputs
print("=" * 80)
print(f"PROJECT FORGE - Phase {args.phase}")
print("=" * 80)

# Status outputs with checkmarks
print(f"✓ Refined concept:")
print(f"✓ Learning goals:")
print(f"✓ Plan approved after {iteration} iteration(s)!")

# Summary tables
print("=" * 80)
print("PLANNING SUMMARY")
print("=" * 80)
print("PROJECT CONCEPT:")
print(f"  {result.project_idea.refined_summary}")
print("\nLEARNING GOALS:")
for i, goal in enumerate(result.project_goals.learning_goals, 1):
    print(f"  {i}. {goal}")
```

### 5.5 Progress Tracking

The system tracks progress through iteration counts:

```python
# From evaluator_agent.py
iteration = 1
while iteration <= max_iterations:
    print(f"\n--- Iteration {iteration}/{max_iterations} ---\n")
    
    # ... refinement logic ...
    
    if evaluation_result.approved:
        print(f"✓ Plan approved after {iteration} iteration(s)!\n")
        break
    elif iteration < max_iterations:
        print(f"Plan needs refinement. Starting iteration {iteration + 1}...\n")
        iteration += 1
    else:
        print(f"Max iterations reached. Using best-effort plan.\n")
        evaluation_result.approved = True
        break

# Final result includes iterations count
return FullPlanResult(
    project_plan=project_plan,
    evaluation=evaluation_result,
    iterations=iteration
)
```

---

## 6. EXISTING UI COMPONENTS

### Current State: CLI-Only (No Web UI Yet)

**Current Interface:** Command-line tool via `runner.py`

### 6.1 CLI Interface

**Location:** `/home/user/Readme-Builder/project_forge/src/orchestration/runner.py`

**Usage:**
```bash
python -m src.orchestration.runner "Build a Streamlit app for tracking habits"
python -m src.orchestration.runner --skill beginner "Create a todo list"
python -m src.orchestration.runner --phase 2 --verbose "Build a REST API"
```

**CLI Arguments:**
```
usage: runner.py [-h] [--skill {beginner,intermediate,advanced}]
                 [--complexity {low,medium,high}] [--time TIME]
                 [--project-type {toy,medium,ambitious}]
                 [--output-dir OUTPUT_DIR] [--verbose]
                 [--phase {2,3,4}]
                 [--log-level {DEBUG,INFO,WARNING,ERROR}]
                 [idea]

positional arguments:
  idea                  The raw project idea (can also be piped via stdin)

optional arguments:
  --skill {beginner,intermediate,advanced}
                        Your skill level (default: intermediate)
  --complexity {low,medium,high}
                        Desired project complexity (default: medium)
  --time TIME           Time constraint (default: "1-2 weeks")
  --project-type {toy,medium,ambitious}
                        Project scope (default: medium)
  --output-dir OUTPUT_DIR
                        Directory to save README/PRD (default: output)
  --verbose             Enable verbose logging
  --phase {2,3,4}       Which phase to run (default: 4)
  --log-level {DEBUG,INFO,WARNING,ERROR}
                        Logging level (default: INFO)
```

### 6.2 Output Formats

**Standard Text Output:**
- Human-readable summaries to console
- Progress indicators (✓ checks, phase numbers)
- Formatted tables and lists

**File Output (Phase 4+):**
- README/PRD markdown files saved to `output/` directory
- Naming pattern: `{project_name}_README.md`
- Example: `HABIT_TRACKER_APP_README.md`

### 6.3 Framework Templates (Configuration)

**Location:** `/home/user/Readme-Builder/project_forge/src/config/defaults.yaml`

While not a UI, the configuration provides template-driven customization:
- Skill level presets (beginner, intermediate, advanced)
- Framework templates (minimal_cli, streamlit_app, rest_api, full_stack, agent_system)
- Project type presets (toy, medium, ambitious)
- Agent behavior parameters

### 6.4 No Existing UI Components

**NOT Present:**
- Streamlit web interface
- Flask/Django web application
- React frontend
- API server for querying agents
- Database for storing plans/history
- Web dashboard for visualization

**Opportunity for New UI:**
The Streamlit UI you're building could display:
1. Agent execution status and progress
2. Intermediate outputs from each agent
3. Reasoning chains and decision points
4. Rubric scores and evaluation feedback
5. Plan visualization (phases, steps, dependencies)
6. Interactive plan modification interface
7. README preview and export options
8. History and comparison of generated plans

---

## 7. TOOL MODULES AND UTILITIES

### 7.1 Rubric Tool (Evaluation Framework)

**Location:** `/home/user/Readme-Builder/project_forge/src/tools/rubric_tool.py`

**Purpose:** Structured evaluation and scoring of project plans.

**Key Components:**
```python
class RubricCriterion(Enum):
    CLARITY = "clarity"
    FEASIBILITY = "feasibility"
    TEACHING_VALUE = "teaching_value"
    TECHNICAL_DEPTH = "technical_depth"
    COMPLETENESS = "completeness"
    BALANCE = "balance"

@dataclass
class RubricScore:
    criterion: RubricCriterion
    score: int                  # 0-10
    feedback: str
    pass_threshold: int = 7
    
    def passes(self) -> bool

@dataclass
class RubricEvaluation:
    component: str
    scores: List[RubricScore]
    overall_pass: bool
    summary: str
    recommendations: List[str]
```

**Evaluation Functions:**
```python
evaluate_concept_clarity(summary: str) -> RubricScore
evaluate_phase_balance(phases: List[Phase]) -> RubricScore
evaluate_teaching_clarity(plan: ProjectPlan, skill_level: str) -> RubricScore
evaluate_technical_depth(plan: ProjectPlan, skill_level: str) -> RubricScore
evaluate_feasibility_for_project_type(plan: ProjectPlan, project_type: str, time_constraint: str) -> RubricScore
```

### 7.2 Consistency Tool

**Location:** `/home/user/Readme-Builder/project_forge/src/tools/consistency_tool.py`

**Purpose:** Structural validation of project plans.

**Key Components:**
```python
@dataclass
class ConsistencyIssue:
    severity: str              # 'error' or 'warning'
    category: str
    message: str
    location: str              # e.g., 'Phase 2, Step 5'

@dataclass
class ConsistencyReport:
    issues: List[ConsistencyIssue]
    passed: bool
    summary: str
    
    def has_errors(self) -> bool
    def has_warnings(self) -> bool
    def get_error_count(self) -> int
    def get_warning_count(self) -> int
```

**Validation Functions:**
```python
validate_project_plan(plan: ProjectPlan) -> ConsistencyReport
check_phase_count(phases: List[Phase], expected_count: int = 5) -> ConsistencyReport
check_step_numbering(phases: List[Phase]) -> ConsistencyReport
check_step_dependencies(phases: List[Phase]) -> ConsistencyReport
```

### 7.3 Text Cleaner Tool

**Location:** `/home/user/Readme-Builder/project_forge/src/tools/text_cleaner_tool.py`

**Purpose:** Clean and normalize user input.

**Functions:**
```python
normalize_whitespace(text: str) -> str
remove_filler_words(text: str) -> str
expand_common_abbreviations(text: str) -> str
clean_project_idea(raw_idea: str) -> str         # Main entry point
extract_keywords(text: str) -> List[str]
```

---

## 8. DATA FLOW AND INTEGRATION EXAMPLE

### Complete End-to-End Flow

```
USER INPUT (CLI)
    "Build a Streamlit dashboard for habit tracking"
        ↓
TEXT CLEANER
    → clean_project_idea()
    → extract_keywords()
    → "Build a Streamlit dashboard for tracking habits"
        ↓
CONCEPT EXPANDER AGENT
    INPUT: raw_description + skill_level + keywords
    LLM PROCESS: expand vague idea
    OUTPUT: ProjectIdea(
        raw_description="Build a Streamlit dashboard...",
        refined_summary="A web application that visualizes and tracks user habits...",
        constraints={"time": "2 weeks", "complexity": "medium", ...}
    )
    DISPLAY: ✓ Clarity score: 8/10
        ↓
GOALS ANALYZER AGENT
    INPUT: ProjectIdea + skill_level
    LLM PROCESS: extract learning and technical goals
    OUTPUT: ProjectGoals(
        learning_goals=["State management in Streamlit", "Data visualization", ...],
        technical_goals=["Web app with persistence", "Interactive UI", ...],
        priority_notes="Focus on core functionality"
    )
    DISPLAY: ✓ 3 learning goals, 3 technical goals
        ↓
FRAMEWORK SELECTOR AGENT
    INPUT: ProjectIdea + ProjectGoals + skill_level
    LLM PROCESS: recommend tech stack
    CONFIG: load_framework_config() reads defaults.yaml
    OUTPUT: FrameworkChoice(
        frontend="Streamlit",
        backend="Python",
        storage="SQLite",
        special_libs=["pandas", "plotly"]
    )
    DISPLAY: ✓ Frontend: Streamlit, Backend: Python
        ↓
PHASE DESIGNER AGENT
    INPUT: ProjectIdea + ProjectGoals + FrameworkChoice + skill_level
    LLM PROCESS: create 5-phase plan with ~50 steps
    OUTPUT: List[Phase] with Step objects
        Phase(1, "Setup", [Step(1, ...), Step(2, ...), ...])
        Phase(2, "Core Features", [...])
        ...
    DISPLAY: ✓ Created 5 phases with 50 total steps
        ↓
TEACHER AGENT
    INPUT: Phases + ProjectGoals + skill_level
    LLM PROCESS: add "what you'll learn" to each step
    OUTPUT: Same phases with what_you_learn field populated + global_teaching_notes
    DISPLAY: ✓ Added teaching annotations to 48/50 steps
        ↓
PROJECT PLAN ASSEMBLY
    ProjectPlan = ProjectIdea + ProjectGoals + FrameworkChoice + Phases + Teaching Notes
        ↓
EVALUATOR AGENT
    INPUT: ProjectPlan + skill_level + project_type + time_constraint
    PROCESS:
        1. Heuristic evaluation (rubrics)
        2. Consistency checking
        3. Scope validation
    OUTPUT: EvaluationResult(
        approved=True,
        scores={CLARITY: 9/10, FEASIBILITY: 8/10, ...},
        feedback="Plan approved! ✓",
        ...
    )
    DISPLAY: ✓ Plan approved after 1 iteration(s)!
        ↓
[IF NOT APPROVED: Return to PhaseDesigner for refinement, max 2 iterations]
        ↓
PRD WRITER AGENT
    INPUT: ProjectPlan
    LLM PROCESS: convert to markdown narrative
    CONFIG: Template structure from _build_readme_template()
    OUTPUT: README markdown text (~8000-10000 lines)
    DISPLAY: ✓ README generated (8400 characters)
        ↓
FILE OUTPUT (Phase 4)
    Save to: /home/user/Readme-Builder/output/HABIT_TRACKER_APP_README.md
    DISPLAY: README/PRD written to: output/HABIT_TRACKER_APP_README.md
        ↓
FINAL SUMMARY
    Shows plan overview, evaluation scores, file location, next steps
```

---

## 9. KEY ARCHITECTURAL PATTERNS

### 9.1 Sequential Agent Pipeline

Unlike parallel agent systems, this architecture runs agents sequentially:
- Each agent completes before the next begins
- Explicit data passing between agents
- Allows for error checking and iteration loops

### 9.2 Structured Output Parsing

Every agent produces JSON-formatted output that's parsed to data models:
- Provides type safety
- Enables composition and chaining
- Fallback strategies for parse failures

### 9.3 Separation of Concerns

- **Data Models:** Pure data structures (project_models.py)
- **Agents:** Reasoning and decision-making (agent files)
- **Tools:** Utilities for evaluation/cleaning (tools/)
- **Orchestration:** Pipeline coordination (crew_config.py, runner.py)

### 9.4 Evaluation Loop

Plans can undergo multiple iterations if they don't meet quality thresholds:
- EvaluatorAgent provides feedback
- PhaseDesigner can refactor
- TeacherAgent re-enriches
- Maximum 2-3 iterations to prevent API cost explosion

### 9.5 Configuration-Driven Behavior

Framework choices and agent behavior are influenced by:
- defaults.yaml (framework templates, skill presets, agent parameters)
- CLI arguments (skill level, project type, time constraint)
- Agent backstories (personality and philosophy)

---

## 10. IMPLEMENTATION RECOMMENDATIONS FOR STREAMLIT UI

Based on this architecture, here's what a Streamlit UI should track:

### Recommended UI Elements

**1. Execution Status Dashboard**
- Real-time progress (which agent is running)
- Estimated time remaining
- Token usage tracking (OpenAI API calls)

**2. Agent-by-Agent Breakdown**
- ConceptExpander: Show refined_summary, constraints
- GoalsAnalyzer: Display learning_goals, technical_goals
- FrameworkSelector: Show frontend/backend/storage choices
- PhaseDesigner: Display phase structure and step counts
- TeacherAgent: Show teaching annotation completion %
- EvaluatorAgent: Display scores, approval status, feedback
- PRDWriter: Show README generation progress

**3. Intermediate Data Visualization**
- JSON tree view of ProjectIdea, ProjectGoals, etc.
- Phase timeline visualization
- Step dependency graph
- Rubric score charts

**4. Iteration Tracking**
- Current iteration number
- Evaluation feedback for each iteration
- Critical issues list
- Suggestions list

**5. Output Preview**
- Live markdown preview of README
- Export options (markdown, PDF, etc.)
- Copy to clipboard functionality

**6. History and Comparison**
- Previous runs
- Side-by-side plan comparison
- Refinement history

### Data Structures to Display (in UI)

```python
# Core display objects
display_data = {
    "current_phase": 2,              # Which phase (1-4) running
    "current_agent": "GoalsAnalyzer",
    "start_time": datetime,
    "elapsed_time": float,
    
    "planning_result": PlanningResult,
    "full_plan_result": FullPlanResult,
    "final_result": FullPlanWithReadmeResult,
    
    "iteration": int,
    "max_iterations": int,
    
    "evaluation_result": EvaluationResult,
    "status": "running" | "completed" | "error",
    "error_message": str or None,
    
    "readme_content": str,
    "project_name": str
}
```

---

## SUMMARY TABLE: All Agents and Their Contracts

| Agent | Input Model(s) | Output Model(s) | Parsing Function | Failure Mode |
|-------|---|---|---|---|
| ConceptExpander | raw text string | ProjectIdea | parse_concept_expansion_result | Falls back to raw text as summary |
| GoalsAnalyzer | ProjectIdea | ProjectGoals | parse_goals_analysis_result | Empty goals with error note |
| FrameworkSelector | ProjectIdea + ProjectGoals | FrameworkChoice | parse_framework_selection_result | Safe defaults (Streamlit + Python) |
| PhaseDesigner | ProjectIdea + ProjectGoals + FrameworkChoice | List[Phase] | parse_phase_design_result | TBD - would need graceful degradation |
| TeacherAgent | List[Phase] + ProjectGoals | Enriched phases + teaching_notes | parse_teaching_enrichment_result | Empty teaching notes |
| EvaluatorAgent | ProjectPlan | EvaluationResult | N/A (heuristic evaluation) | Returns scores + critical_issues |
| PRDWriter | ProjectPlan | str (markdown) | parse_prd_writing_result | Returns error message instead of content |

---

