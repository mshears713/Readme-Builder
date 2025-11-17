"""
CrewAI configuration and orchestration for Project Forge.

This module sets up the multi-agent crew including all agents, tasks, and
the execution flow. It wires together ConceptExpander, GoalsAnalyzer,
FrameworkSelector, PhaseDesigner, TeacherAgent, EvaluatorAgent, and
PRDWriterAgent into a cohesive pipeline.

Phase 1: This is a stub implementation with placeholder agent definitions.
Real agent logic will be implemented in Phase 2 and Phase 3.
"""

from typing import List, Optional
from dataclasses import dataclass


@dataclass
class AgentConfig:
    """
    Configuration for a single agent.

    Attributes:
        name: Agent identifier
        role: What this agent does in the system
        goal: What this agent is trying to achieve
        backstory: Context that shapes agent behavior
        tools: List of tool names this agent can use
        verbose: Whether to log agent actions
    """
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
    """
    Configuration for a single task.

    Attributes:
        name: Task identifier
        description: What needs to be done
        expected_output: Description of the output format
        agent: Which agent executes this task
        context: List of previous tasks this depends on
    """
    name: str
    description: str
    expected_output: str
    agent: str  # Agent name
    context: List[str] = None  # Names of prerequisite tasks

    def __post_init__(self):
        if self.context is None:
            self.context = []


# AGENT DEFINITIONS (Stubs for Phase 1)
# These will be fleshed out with real CrewAI Agent objects in Phase 2

def get_concept_expander_config() -> AgentConfig:
    """
    Define ConceptExpanderAgent configuration.

    This agent takes raw user input and expands it into a clear, structured
    project concept. Uses text_cleaner_tool to normalize input.
    """
    return AgentConfig(
        name="concept_expander",
        role="Project Concept Expander",
        goal="Transform raw project ideas into clear, structured concepts",
        backstory="""You are an expert at taking vague, messy project ideas and
        turning them into clear, actionable project concepts. You ask the right
        questions, identify constraints, and remove ambiguity while preserving
        the user's original intent.""",
        tools=["text_cleaner"],
        verbose=True
    )


def get_goals_analyzer_config() -> AgentConfig:
    """
    Define GoalsAnalyzerAgent configuration.

    Extracts learning goals (what concepts to learn) and technical goals
    (what to build) from the refined project concept.
    """
    return AgentConfig(
        name="goals_analyzer",
        role="Learning & Technical Goals Analyst",
        goal="Extract clear learning objectives and technical deliverables",
        backstory="""You are a skilled educator and technical architect who can
        identify both what someone will learn from a project and what they will
        build. You think in terms of skill development and concrete outcomes.""",
        tools=[],
        verbose=True
    )


def get_framework_selector_config() -> AgentConfig:
    """
    Define FrameworkSelectorAgent configuration.

    Chooses appropriate technology stack based on project goals, user skill
    level, and complexity constraints.
    """
    return AgentConfig(
        name="framework_selector",
        role="Technology Stack Advisor",
        goal="Select appropriate frameworks and tools for the project",
        backstory="""You are a pragmatic tech lead who knows when to use simple
        tools vs complex ones. You prioritize developer experience, learning value,
        and choosing well-documented, stable technologies. You match tools to
        skill levels appropriately.""",
        tools=[],
        verbose=True
    )


def get_phase_designer_config() -> AgentConfig:
    """
    Define PhaseDesignerAgent configuration.

    Creates 5 phases with ~10 steps each, organizing the project into
    a structured, sequential build plan.
    """
    return AgentConfig(
        name="phase_designer",
        role="Project Phase Architect",
        goal="Design a 5-phase, 50-step build plan",
        backstory="""You are a master project planner who breaks down complex
        projects into manageable phases and concrete steps. You ensure each step
        is small enough to be achievable but substantial enough to make progress.
        You think about dependencies and logical ordering.""",
        tools=["consistency_checker"],
        verbose=True
    )


def get_teacher_agent_config() -> AgentConfig:
    """
    Define TeacherAgent configuration.

    Enriches phases and steps with teaching annotations explaining what
    the user will learn and why each step matters.
    """
    return AgentConfig(
        name="teacher",
        role="Educational Enrichment Specialist",
        goal="Add teaching value and learning context to the project plan",
        backstory="""You are an experienced programming educator who knows how to
        turn any project into a learning experience. You explain not just what to
        do, but why, what patterns are involved, and what skills are being developed.
        You make every step a mini-lesson.""",
        tools=[],
        verbose=True
    )


def get_evaluator_agent_config() -> AgentConfig:
    """
    Define EvaluatorAgent configuration.

    Reviews the project plan for clarity, feasibility, teaching value, and
    consistency. Approves or requests revisions.
    """
    return AgentConfig(
        name="evaluator",
        role="Project Plan Quality Evaluator",
        goal="Ensure the plan is clear, feasible, and valuable",
        backstory="""You are a rigorous reviewer who checks project plans for
        quality. You evaluate clarity, feasibility, teaching value, and internal
        consistency. You provide constructive feedback and approve plans that
        meet high standards.""",
        tools=["rubric_evaluator", "consistency_checker"],
        verbose=True
    )


def get_prd_writer_config() -> AgentConfig:
    """
    Define PRDWriterAgent configuration.

    Converts the structured ProjectPlan into a comprehensive README/PRD
    document that can be fed to Claude Code or another code LLM.
    """
    return AgentConfig(
        name="prd_writer",
        role="README/PRD Documentation Writer",
        goal="Generate comprehensive, actionable project documentation",
        backstory="""You are a technical writer who creates excellent README files
        and project requirement documents. You know how to structure information
        so it's clear, complete, and ready for implementation. Your docs make it
        easy for any developer (or AI) to build the project.""",
        tools=[],
        verbose=True
    )


# TASK DEFINITIONS (Stubs for Phase 1)

def get_concept_expansion_task() -> TaskConfig:
    """Define the task for expanding raw ideas into structured concepts."""
    return TaskConfig(
        name="concept_expansion",
        description="Take the raw project idea and expand it into a clear, structured concept",
        expected_output="A ProjectIdea object with refined_summary and constraints",
        agent="concept_expander",
        context=[]
    )


def get_goals_analysis_task() -> TaskConfig:
    """Define the task for extracting learning and technical goals."""
    return TaskConfig(
        name="goals_analysis",
        description="Analyze the refined concept and extract learning and technical goals",
        expected_output="A ProjectGoals object with learning_goals and technical_goals",
        agent="goals_analyzer",
        context=["concept_expansion"]
    )


def get_framework_selection_task() -> TaskConfig:
    """Define the task for selecting technology stack."""
    return TaskConfig(
        name="framework_selection",
        description="Choose appropriate frameworks and tools based on goals and skill level",
        expected_output="A FrameworkChoice object with frontend, backend, storage, and special_libs",
        agent="framework_selector",
        context=["concept_expansion", "goals_analysis"]
    )


def get_phase_design_task() -> TaskConfig:
    """Define the task for designing phases and steps."""
    return TaskConfig(
        name="phase_design",
        description="Create a 5-phase, 50-step build plan for the project",
        expected_output="A list of 5 Phase objects, each with ~10 Step objects",
        agent="phase_designer",
        context=["concept_expansion", "goals_analysis", "framework_selection"]
    )


def get_teaching_enrichment_task() -> TaskConfig:
    """Define the task for adding teaching annotations."""
    return TaskConfig(
        name="teaching_enrichment",
        description="Enrich phases and steps with learning notes and teaching commentary",
        expected_output="Updated phases with what_you_learn fields and teaching_notes",
        agent="teacher",
        context=["phase_design"]
    )


def get_evaluation_task() -> TaskConfig:
    """Define the task for evaluating the complete plan."""
    return TaskConfig(
        name="evaluation",
        description="Evaluate the complete project plan for quality and consistency",
        expected_output="RubricEvaluation and ConsistencyReport indicating approval or needed revisions",
        agent="evaluator",
        context=["teaching_enrichment"]
    )


def get_prd_writing_task() -> TaskConfig:
    """Define the task for writing the final README/PRD."""
    return TaskConfig(
        name="prd_writing",
        description="Convert the approved ProjectPlan into a comprehensive README/PRD document",
        expected_output="Complete README/PRD markdown text ready to save to disk",
        agent="prd_writer",
        context=["evaluation"]
    )


# CREW ASSEMBLY (Stub for Phase 1)

def get_all_agent_configs() -> List[AgentConfig]:
    """Get all agent configurations for the crew."""
    return [
        get_concept_expander_config(),
        get_goals_analyzer_config(),
        get_framework_selector_config(),
        get_phase_designer_config(),
        get_teacher_agent_config(),
        get_evaluator_agent_config(),
        get_prd_writer_config(),
    ]


def get_all_task_configs() -> List[TaskConfig]:
    """Get all task configurations in execution order."""
    return [
        get_concept_expansion_task(),
        get_goals_analysis_task(),
        get_framework_selection_task(),
        get_phase_design_task(),
        get_teaching_enrichment_task(),
        get_evaluation_task(),
        get_prd_writing_task(),
    ]


def create_crew():
    """
    Create and configure the CrewAI crew.

    This is a stub for Phase 1. In Phase 2, this will instantiate real
    CrewAI Agent and Task objects and wire them together.

    Returns:
        Configured crew ready to run (stub implementation returns None)
    """
    # Phase 1 stub - will be implemented in Phase 2
    print("Crew configuration loaded (stub - will be implemented in Phase 2)")
    return None
