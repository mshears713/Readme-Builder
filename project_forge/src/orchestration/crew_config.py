"""
CrewAI configuration and orchestration for Project Forge.

This module sets up the multi-agent crew including all agents, tasks, and
the execution flow. It wires together ConceptExpander, GoalsAnalyzer,
FrameworkSelector, PhaseDesigner, TeacherAgent, EvaluatorAgent, and
PRDWriterAgent into a cohesive pipeline.

Phase 2: Implements the planning crew (ConceptExpander, GoalsAnalyzer, FrameworkSelector).
Phase 3 will add: PhaseDesigner, TeacherAgent, EvaluatorAgent.
Phase 4 will add: PRDWriterAgent.
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from crewai import Crew

from ..models.project_models import ProjectIdea, ProjectGoals, FrameworkChoice
from ..agents.concept_expander_agent import (
    create_concept_expander_agent,
    create_concept_expansion_task,
    parse_concept_expansion_result
)
from ..agents.goals_analyzer_agent import (
    create_goals_analyzer_agent,
    create_goals_analysis_task,
    parse_goals_analysis_result
)
from ..agents.framework_selector_agent import (
    create_framework_selector_agent,
    create_framework_selection_task,
    parse_framework_selection_result
)
from ..tools.rubric_tool import evaluate_concept_clarity


@dataclass
class PlanningResult:
    """
    Result from the planning crew (Phase 2).

    Contains the outputs from ConceptExpander, GoalsAnalyzer, and
    FrameworkSelector, plus any evaluation metadata.

    Attributes:
        project_idea: Refined concept with constraints
        project_goals: Learning and technical objectives
        framework_choice: Selected technology stack
        clarity_score: Rubric score for concept clarity
    """
    project_idea: ProjectIdea
    project_goals: ProjectGoals
    framework_choice: FrameworkChoice
    clarity_score: Optional[Any] = None


def create_planning_crew(raw_idea: str, skill_level: str = "intermediate", verbose: bool = True) -> PlanningResult:
    """
    Create and run the planning crew (Phase 2).

    This crew executes the first three agents in sequence:
    1. ConceptExpanderAgent: raw idea → refined ProjectIdea
    2. GoalsAnalyzerAgent: ProjectIdea → ProjectGoals
    3. FrameworkSelectorAgent: ProjectIdea + ProjectGoals → FrameworkChoice

    Args:
        raw_idea: Raw project idea from user input
        skill_level: User's skill level (beginner/intermediate/advanced)
        verbose: Whether to print detailed agent execution logs

    Returns:
        PlanningResult with all planning outputs

    Teaching Note:
        In CrewAI, agents don't directly pass objects to each other. Instead,
        each task produces text output that the next task can reference. This
        means we need to:
        1. Execute tasks sequentially (not as a Crew, which is async)
        2. Parse each agent's output into our structured models
        3. Pass those models to the next agent's task

        This approach gives us more control over data flow and error handling,
        which is important for a teaching system where we want to show
        intermediate results and catch issues early.
    """
    print("\n" + "=" * 80)
    print("PLANNING CREW - Phase 2")
    print("=" * 80 + "\n")

    # STEP 1: Concept Expansion
    # Take raw idea and clean/expand it into a structured concept
    print("STEP 1/3: Expanding project concept...")
    print(f"Raw idea: {raw_idea}\n")

    concept_agent = create_concept_expander_agent()
    concept_task = create_concept_expansion_task(concept_agent, raw_idea, skill_level)
    concept_result = concept_task.execute()

    # Parse into ProjectIdea
    project_idea = parse_concept_expansion_result(concept_result, raw_idea)

    print(f"✓ Refined concept:")
    print(f"  {project_idea.refined_summary}\n")
    print(f"  Constraints: {project_idea.constraints}\n")

    # Evaluate clarity using rubric tool
    clarity_score = evaluate_concept_clarity(project_idea.refined_summary)
    print(f"  Clarity score: {clarity_score.score}/10")
    print(f"  Feedback: {clarity_score.feedback}\n")

    # STEP 2: Goals Analysis
    # Extract learning and technical goals from the refined concept
    print("STEP 2/3: Analyzing learning and technical goals...")

    goals_agent = create_goals_analyzer_agent()
    goals_task = create_goals_analysis_task(goals_agent, project_idea, skill_level)
    goals_result = goals_task.execute()

    # Parse into ProjectGoals
    project_goals = parse_goals_analysis_result(goals_result)

    print(f"✓ Learning goals:")
    for goal in project_goals.learning_goals:
        print(f"  - {goal}")
    print(f"\n✓ Technical goals:")
    for goal in project_goals.technical_goals:
        print(f"  - {goal}")
    print(f"\n  Priority: {project_goals.priority_notes}\n")

    # STEP 3: Framework Selection
    # Choose appropriate tech stack based on concept and goals
    print("STEP 3/3: Selecting technology stack...")

    framework_agent = create_framework_selector_agent()
    framework_task = create_framework_selection_task(
        framework_agent,
        project_idea,
        project_goals,
        skill_level
    )
    framework_result = framework_task.execute()

    # Parse into FrameworkChoice
    framework_choice = parse_framework_selection_result(framework_result)

    print(f"✓ Selected frameworks:")
    print(f"  Frontend: {framework_choice.frontend or 'None (CLI-only)'}")
    print(f"  Backend:  {framework_choice.backend or 'None'}")
    print(f"  Storage:  {framework_choice.storage or 'None'}")
    if framework_choice.special_libs:
        print(f"  Libraries: {', '.join(framework_choice.special_libs)}")
    print()

    print("=" * 80)
    print("PLANNING COMPLETE")
    print("=" * 80 + "\n")

    return PlanningResult(
        project_idea=project_idea,
        project_goals=project_goals,
        framework_choice=framework_choice,
        clarity_score=clarity_score
    )


# Legacy config objects (kept for Phase 1 compatibility, will be removed in Phase 3)

@dataclass
class AgentConfig:
    """Legacy configuration object for Phase 1 compatibility."""
    name: str
    role: str
    goal: str
    backstory: str = ""
    tools: List[str] = None
    verbose: bool = True

    def __post_init__(self):
        if self.tools is None:
            self.tools = []


@dataclass
class TaskConfig:
    """Legacy configuration object for Phase 1 compatibility."""
    name: str
    description: str
    expected_output: str
    agent: str
    context: List[str] = None

    def __post_init__(self):
        if self.context is None:
            self.context = []


def create_crew():
    """
    Legacy crew creation function (Phase 1 compatibility).

    Phase 2 uses create_planning_crew() instead, which provides better
    control over sequential execution and intermediate outputs.

    Returns:
        None (legacy stub)
    """
    print("Note: Use create_planning_crew() for Phase 2 functionality")
    return None
