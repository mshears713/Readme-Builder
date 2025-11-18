"""Core data models passed between Project Forge agents."""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class ProjectIdea:
    """
    Raw and refined representation of the user's project idea.

    This model is populated by ConceptExpanderAgent, which takes the raw user input
    and expands it into a structured, clear project concept. The refined_summary
    removes noise and ambiguity. Constraints help later agents choose appropriate
    frameworks and scope.

    Attributes:
        raw_description: The original idea string from the user's CLI input
        refined_summary: Cleaned, expanded version with context and clarity
        constraints: Dict of project constraints (e.g., {'time': '1 week', 'complexity': 'medium'})
    """
    raw_description: str
    refined_summary: str = ""
    constraints: Dict[str, Any] = field(default_factory=dict)  # time, complexity, hardware, etc.


@dataclass
class ProjectGoals:
    """
    Learning and technical objectives extracted from the project idea.

    GoalsAnalyzerAgent populates this model by analyzing the refined ProjectIdea
    and extracting what end-users should learn from USING the program (concepts,
    patterns they'll encounter) and what the program should do (technical deliverables).
    These goals guide framework selection and educational feature design.

    Attributes:
        learning_goals: List of concepts/skills end-users will learn by USING the program
                       (e.g., "understand async patterns through interactive demos")
        technical_goals: List of technical deliverables the program provides
                        (e.g., "REST API with documentation", "interactive web scraper tutorial")
        priority_notes: Notes on which goals are most important or time-sensitive
    """
    learning_goals: List[str] = field(default_factory=list)
    technical_goals: List[str] = field(default_factory=list)
    priority_notes: str = ""


@dataclass
class FrameworkChoice:
    """
    Technology stack recommendations based on project goals and skill level.

    FrameworkSelectorAgent chooses appropriate tools and libraries that match
    the user's skill level, project complexity, and learning goals. Prefers
    simple, well-documented options for beginners.

    Attributes:
        frontend: UI framework if needed (e.g., "Streamlit", "Flask+HTML", None for CLI-only)
        backend: Server/API framework (e.g., "FastAPI", "Flask", None for scripts)
        storage: Data persistence approach (e.g., "SQLite", "JSON files", "Postgres")
        special_libs: Domain-specific libraries (e.g., ["CrewAI", "LangChain", "BeautifulSoup"])
    """
    frontend: Optional[str] = None  # e.g., Streamlit, None
    backend: Optional[str] = None   # e.g., FastAPI, CLI-only
    storage: Optional[str] = None   # e.g., SQLite, files
    special_libs: List[str] = field(default_factory=list)  # CrewAI, LangChain, etc.


@dataclass
class Step:
    """
    A single implementation step within a phase.

    Steps are small, concrete tasks that PhaseDesignerAgent creates and TeacherAgent
    enriches with educational feature guidance. Each step should be completable in
    a short session. Dependencies track which steps must be completed first.

    Attributes:
        index: Unique step number (global across all phases)
        title: Short, actionable step name (e.g., "Create user authentication endpoint")
        description: Detailed instructions for what to build in this step
        teaching_guidance: Instructions for implementing agent on what educational features to build
        dependencies: List of step indices that must be completed before this one
        what_you_learn: Legacy alias kept for backwards compatibility with docs/examples
    """

    index: int
    title: str
    description: str = ""
    teaching_guidance: str = ""
    dependencies: List[int] = field(default_factory=list)  # indices of prerequisite steps
    what_you_learn: str = ""

    def __post_init__(self) -> None:
        """Keep legacy `what_you_learn` and the canonical teaching field in sync."""

        if self.what_you_learn and not self.teaching_guidance:
            object.__setattr__(self, "teaching_guidance", self.what_you_learn)
        elif self.teaching_guidance and not self.what_you_learn:
            object.__setattr__(self, "what_you_learn", self.teaching_guidance)

    def __setattr__(self, name: str, value: Any) -> None:
        """Ensure both naming conventions always match for downstream consumers."""

        object.__setattr__(self, name, value)
        if name == "teaching_guidance":
            object.__setattr__(self, "what_you_learn", value)
        elif name == "what_you_learn":
            object.__setattr__(self, "teaching_guidance", value)


@dataclass
class Phase:
    """
    A major milestone in the project, containing multiple steps.

    Phases organize the build plan into logical stages (e.g., "Setup", "Core Features",
    "Polish"). PhaseDesignerAgent creates 5 phases with ~10 steps each. Each phase
    represents a coherent chunk of work with a clear deliverable.

    Attributes:
        index: Phase number (1-5 in standard plans)
        name: Descriptive phase name (e.g., "Foundations & Models", "Core API")
        description: Overview of what this phase accomplishes and why
        steps: List of Step objects that make up this phase
    """
    index: int
    name: str
    description: str = ""
    steps: List[Step] = field(default_factory=list)


@dataclass
class ProjectPlan:
    """
    Complete project plan including idea, goals, frameworks, and phases.

    This is the final structured output from all agents working together.
    It contains everything needed to generate a comprehensive README/PRD that
    a code LLM can execute. PRDWriterAgent converts this into narrative form.

    Attributes:
        idea: The refined project concept (from ConceptExpanderAgent)
        goals: Learning and technical objectives (from GoalsAnalyzerAgent)
        framework: Technology stack choices (from FrameworkSelectorAgent)
        phases: 5 phases containing ~50 total steps (from PhaseDesignerAgent + TeacherAgent)
        teaching_notes: Global pedagogical commentary on the overall learning arc
    """
    idea: ProjectIdea
    goals: ProjectGoals
    framework: FrameworkChoice
    phases: List[Phase] = field(default_factory=list)
    teaching_notes: str = ""  # global pedagogical notes
