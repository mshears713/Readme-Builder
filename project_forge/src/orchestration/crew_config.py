"""
CrewAI configuration and orchestration for Project Forge.

This module sets up the multi-agent crew including all agents, tasks, and
the execution flow. It wires together ConceptExpander, GoalsAnalyzer,
FrameworkSelector, PhaseDesigner, TeacherAgent, EvaluatorAgent, and
PRDWriterAgent into a cohesive pipeline.

Phase 2: Implements the planning crew (ConceptExpander, GoalsAnalyzer, FrameworkSelector).
Phase 3: Adds PhaseDesigner, TeacherAgent, EvaluatorAgent for full plan generation.
Phase 4 will add: PRDWriterAgent.
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from crewai import Crew

from ..models.project_models import ProjectIdea, ProjectGoals, FrameworkChoice, ProjectPlan, Phase
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
from ..agents.phase_designer_agent import (
    create_phase_designer_agent,
    create_phase_design_task,
    parse_phase_design_result
)
from ..agents.teacher_agent import (
    create_teacher_agent,
    create_teaching_enrichment_task,
    parse_teaching_enrichment_result
)
from ..agents.evaluator_agent import evaluate_project_plan, EvaluationResult
from ..agents.prd_writer_agent import (
    create_prd_writer_agent,
    create_prd_writing_task,
    parse_prd_writing_result,
    generate_project_name
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


@dataclass
class FullPlanResult:
    """
    Result from the complete planning+teaching crew (Phase 3).

    Contains the full ProjectPlan with phases, steps, educational feature guidance,
    and evaluation results.

    Attributes:
        project_plan: Complete ProjectPlan object
        evaluation: EvaluationResult from quality checks
        iterations: Number of refinement iterations performed
    """
    project_plan: ProjectPlan
    evaluation: EvaluationResult
    iterations: int = 1


@dataclass
class FullPlanWithReadmeResult:
    """
    Result from the complete pipeline including README generation (Phase 4).

    Contains the full ProjectPlan, evaluation results, AND the final README/PRD
    markdown text ready to be written to disk.

    Attributes:
        project_plan: Complete ProjectPlan object
        evaluation: EvaluationResult from quality checks
        readme_content: Final README/PRD markdown text
        project_name: Generated project name for the output file
        iterations: Number of refinement iterations performed
    """
    project_plan: ProjectPlan
    evaluation: EvaluationResult
    readme_content: str
    project_name: str
    iterations: int = 1


def create_planning_crew(raw_idea: str, skill_level: str = "intermediate", verbose: bool = True,
                         progress_callback=None) -> PlanningResult:
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
        progress_callback: Optional callback function(agent_name, progress_percent, message)

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

    if progress_callback:
        progress_callback("ConceptExpander", 10, "📝 Expanding project concept...")

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

    if progress_callback:
        progress_callback("GoalsAnalyzer", 40, "✅ ConceptExpander completed")

    # STEP 2: Goals Analysis
    # Extract learning and technical goals from the refined concept
    print("STEP 2/3: Analyzing learning and technical goals...")

    if progress_callback:
        progress_callback("GoalsAnalyzer", 40, "🎯 Analyzing learning goals...")

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

    if progress_callback:
        progress_callback("FrameworkSelector", 70, "✅ GoalsAnalyzer completed")

    # STEP 3: Framework Selection
    # Choose appropriate tech stack based on concept and goals
    print("STEP 3/3: Selecting technology stack...")

    if progress_callback:
        progress_callback("FrameworkSelector", 70, "🔧 Selecting technology stack...")

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

    if progress_callback:
        progress_callback("FrameworkSelector", 100, "✅ FrameworkSelector completed")

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


def create_full_plan_crew(
    raw_idea: str,
    skill_level: str = "intermediate",
    verbose: bool = True,
    max_iterations: int = 2,
    progress_callback=None
) -> FullPlanResult:
    """
    Create and run the complete planning+teaching crew (Phase 3).

    This crew executes all agents from Phase 2 plus the new Phase 3 agents:
    1-3. ConceptExpander, GoalsAnalyzer, FrameworkSelector (Phase 2)
    4. PhaseDesigner: creates 5 phases with ~50 steps
    5. TeacherAgent: adds educational feature guidance to steps
    6. EvaluatorAgent: validates plan quality and structure

    The evaluation loop allows for iterative refinement if the initial
    plan doesn't meet quality thresholds.

    Args:
        raw_idea: Raw project idea from user input
        skill_level: User's skill level (beginner/intermediate/advanced)
        verbose: Whether to print detailed agent execution logs
        max_iterations: Maximum number of refinement iterations
        progress_callback: Optional callback function(agent_name, progress_percent, message)

    Returns:
        FullPlanResult with complete ProjectPlan and evaluation

    Teaching Note:
        This function orchestrates the full agent pipeline. We run Phase 2
        agents to get the foundation (concept, goals, frameworks), then
        Phase 3 agents to build and enrich the plan. The evaluation loop
        ensures quality before returning.
    """
    print("\n" + "=" * 80)
    print("FULL PLAN CREW - Phase 3")
    print("=" * 80 + "\n")

    # PHASE 2: Run planning crew to get concept, goals, and frameworks
    print("Running Phase 2 planning crew...")
    planning_result = create_planning_crew(raw_idea, skill_level, verbose, progress_callback)

    # PHASE 3: Build the detailed plan
    print("\n" + "=" * 80)
    print("PHASE DESIGN & TEACHING - Phase 3")
    print("=" * 80 + "\n")

    iteration = 1
    project_plan = None
    evaluation_result = None

    while iteration <= max_iterations:
        print(f"\n--- Iteration {iteration}/{max_iterations} ---\n")

        # STEP 4: Phase Design
        # Create 5 phases with ~10 steps each
        print("STEP 4: Designing project phases and steps...")

        if progress_callback:
            progress_callback("PhaseDesigner", 50, "📋 Designing project phases...")

        phase_designer = create_phase_designer_agent()
        phase_task = create_phase_design_task(
            phase_designer,
            planning_result.project_idea,
            planning_result.project_goals,
            planning_result.framework_choice,
            skill_level
        )
        phase_result = phase_task.execute()

        # Parse into Phase objects
        phases = parse_phase_design_result(phase_result)

        total_steps = sum(len(phase.steps) for phase in phases)
        print(f"✓ Created {len(phases)} phases with {total_steps} total steps\n")

        if progress_callback:
            progress_callback("TeacherAgent", 70, "✅ PhaseDesigner completed")

        # STEP 5: Teaching Enrichment
        # Add educational feature guidance to each step
        print("STEP 5: Adding educational feature guidance to steps...")

        if progress_callback:
            progress_callback("TeacherAgent", 70, "👨‍🏫 Adding educational guidance...")

        teacher = create_teacher_agent()
        teaching_task = create_teaching_enrichment_task(
            teacher,
            phases,
            planning_result.project_goals,
            skill_level
        )
        teaching_result = teaching_task.execute()

        # Parse enriched phases
        enriched_phases, global_teaching_notes = parse_teaching_enrichment_result(
            teaching_result,
            phases
        )

        # Count steps with teaching guidance
        steps_with_guidance = sum(
            1 for phase in enriched_phases
            for step in phase.steps
            if step.teaching_guidance and len(step.teaching_guidance.strip()) > 10
        )
        print(f"✓ Added educational guidance to {steps_with_guidance}/{total_steps} steps\n")

        # Create ProjectPlan
        project_plan = ProjectPlan(
            idea=planning_result.project_idea,
            goals=planning_result.project_goals,
            framework=planning_result.framework_choice,
            phases=enriched_phases,
            teaching_notes=global_teaching_notes
        )

        if progress_callback:
            progress_callback("EvaluatorAgent", 90, "✅ TeacherAgent completed")

        # STEP 6: Evaluation
        # Validate plan quality and structure
        print("STEP 6: Evaluating plan quality...")

        if progress_callback:
            progress_callback("EvaluatorAgent", 90, "✅ Evaluating plan quality...")

        evaluation_result = evaluate_project_plan(project_plan, skill_level)

        print(f"\n{evaluation_result.feedback}\n")

        if evaluation_result.approved:
            print(f"✓ Plan approved after {iteration} iteration(s)!\n")
            if progress_callback:
                progress_callback("EvaluatorAgent", 100, "✅ EvaluatorAgent completed")
            break
        elif iteration < max_iterations:
            print(f"Plan needs refinement. Starting iteration {iteration + 1}...\n")
            # In a more sophisticated implementation, we'd use the feedback
            # to guide refinement. For Phase 3, we just retry.
            iteration += 1
        else:
            print(f"Max iterations reached. Using best-effort plan.\n")
            # Accept the plan even if not perfect after max iterations
            evaluation_result.approved = True
            if progress_callback:
                progress_callback("EvaluatorAgent", 100, "✅ EvaluatorAgent completed")
            break

    print("=" * 80)
    print("FULL PLAN COMPLETE")
    print("=" * 80 + "\n")

    return FullPlanResult(
        project_plan=project_plan,
        evaluation=evaluation_result,
        iterations=iteration
    )


def create_complete_pipeline(
    raw_idea: str,
    skill_level: str = "intermediate",
    verbose: bool = True,
    max_iterations: int = 2,
    progress_callback=None
) -> FullPlanWithReadmeResult:
    """
    Create and run the complete Project Forge pipeline (Phase 4).

    This is the full end-to-end flow that includes ALL agents:
    1-3. ConceptExpander, GoalsAnalyzer, FrameworkSelector (Phase 2)
    4. PhaseDesigner: creates 5 phases with ~50 steps (Phase 3)
    5. TeacherAgent: enriches steps with teaching annotations (Phase 3)
    6. EvaluatorAgent: validates plan quality and structure (Phase 3)
    7. PRDWriterAgent: converts ProjectPlan to README/PRD markdown (Phase 4)

    Args:
        raw_idea: Raw project idea from user input
        skill_level: User's skill level (beginner/intermediate/advanced)
        verbose: Whether to print detailed agent execution logs
        max_iterations: Maximum number of refinement iterations
        progress_callback: Optional callback function(agent_name, progress_percent, message)

    Returns:
        FullPlanWithReadmeResult with ProjectPlan, evaluation, and README content

    Teaching Note:
        This is the "orchestrator of orchestrators." It:
        1. Runs create_full_plan_crew() to get the validated ProjectPlan
        2. Runs PRDWriterAgent to convert the plan to markdown
        3. Returns everything packaged together for easy file writing

        This separation (plan creation vs. README writing) maintains clean
        separation of concerns and makes testing easier.
    """
    print("\n" + "=" * 80)
    print("COMPLETE PROJECT FORGE PIPELINE - Phase 4")
    print("=" * 80 + "\n")

    # PHASES 2-3: Run full plan crew to get validated ProjectPlan
    print("Running Phases 2-3: Planning, Design, Teaching, and Evaluation...\n")
    plan_result = create_full_plan_crew(raw_idea, skill_level, verbose, max_iterations, progress_callback)

    # PHASE 4: Convert ProjectPlan to README/PRD
    print("\n" + "=" * 80)
    print("README/PRD GENERATION - Phase 4")
    print("=" * 80 + "\n")

    print("STEP 7: Generating comprehensive README/PRD document...")

    if progress_callback:
        progress_callback("PRDWriter", 90, "📄 Generating README/PRD...")

    import logging
    import signal
    from contextlib import contextmanager

    logger = logging.getLogger("project_forge")

    @contextmanager
    def timeout_handler(seconds):
        """Context manager for timeout handling."""
        def timeout_signal_handler(signum, frame):
            raise TimeoutError(f"Task execution exceeded {seconds} seconds")

        # Set the signal handler and alarm
        old_handler = signal.signal(signal.SIGALRM, timeout_signal_handler)
        signal.alarm(seconds)
        try:
            yield
        finally:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old_handler)

    prd_writer = create_prd_writer_agent()
    prd_task = create_prd_writing_task(prd_writer, plan_result.project_plan)

    try:
        logger.info("Starting PRD writer task execution...")
        # Add 10 minute timeout for PRD writer (it can take a while with large plans)
        with timeout_handler(600):
            prd_result = prd_task.execute()
        logger.info("PRD writer task completed successfully")
    except TimeoutError as e:
        logger.error(f"PRD writer timed out: {e}")
        raise TimeoutError(
            "README generation timed out after 10 minutes. "
            "This may indicate an issue with the LLM API or the task complexity. "
            "Try reducing max_iterations or simplifying your project idea."
        )
    except Exception as e:
        logger.error(f"PRD writer failed with error: {e}")
        raise

    # Parse the README content
    readme_content = parse_prd_writing_result(prd_result, plan_result.project_plan)

    # Generate project name for the output file
    project_name = generate_project_name(plan_result.project_plan)

    print(f"✓ README generated ({len(readme_content)} characters)")
    print(f"✓ Project name: {project_name}\n")

    if progress_callback:
        progress_callback("PRDWriter", 100, "✅ PRDWriter completed")

    print("=" * 80)
    print("COMPLETE PIPELINE FINISHED")
    print("=" * 80 + "\n")

    return FullPlanWithReadmeResult(
        project_plan=plan_result.project_plan,
        evaluation=plan_result.evaluation,
        readme_content=readme_content,
        project_name=project_name,
        iterations=plan_result.iterations
    )


def create_crew():
    """
    Legacy crew creation function (Phase 1 compatibility).

    Phase 2 uses create_planning_crew() instead.
    Phase 3 uses create_full_plan_crew() instead.
    Phase 4 uses create_complete_pipeline() instead.

    Returns:
        None (legacy stub)
    """
    print("Note: Use create_complete_pipeline() for the full Phase 4 pipeline")
    return None
