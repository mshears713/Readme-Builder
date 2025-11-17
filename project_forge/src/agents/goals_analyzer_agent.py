"""
GoalsAnalyzerAgent - Extracts learning and technical goals from project concepts.

This agent is the second in the Project Forge pipeline. It receives a refined
ProjectIdea and analyzes it to extract explicit learning goals (what concepts
and skills the user will learn) and technical goals (what they will build).

Key responsibilities:
- Identify learning objectives (concepts, patterns, skills)
- Identify technical deliverables (features, components, capabilities)
- Prioritize goals based on project focus and user needs
- Ensure goals are specific, measurable, and achievable

The output ProjectGoals guides framework selection and teaching enrichment.
"""

from crewai import Agent, Task
from typing import Dict, Any
import json

from ..models.project_models import ProjectIdea, ProjectGoals


def create_goals_analyzer_agent() -> Agent:
    """
    Create the GoalsAnalyzerAgent with specialized prompting for goal extraction.

    This agent acts as both an educator and a technical analyst. It looks at
    a project concept and identifies both the learning value (what skills are
    being practiced) and the technical deliverables (what gets built).

    Returns:
        CrewAI Agent configured for goals analysis

    Teaching Note:
        This agent wears two hats: educator and architect. The educator side
        asks "what will you learn?" while the architect side asks "what will
        you build?". Both perspectives are crucial for creating a project that
        is both functional and educational.
    """
    return Agent(
        role="Learning & Technical Goals Analyst",
        goal="Extract clear learning objectives and technical deliverables from project concepts",
        backstory="""You are a skilled educator and technical architect with a
        unique talent for identifying both the learning value and technical substance
        of any project.

        As an educator, you think in terms of:
        - What concepts and skills are being practiced?
        - What patterns or paradigms will the user encounter?
        - What's the pedagogical arc - what foundation → what advanced skills?
        - Is there a good balance of theory and practice?

        As an architect, you think in terms of:
        - What are the concrete technical deliverables?
        - What components or features need to be built?
        - What technical challenges will the user solve?
        - What's the technical scope and depth?

        You excel at finding the sweet spot where learning goals align with
        technical goals - projects that teach valuable skills while building
        something meaningful and functional.

        You're specific in your goals - never vague. Instead of "learn Python",
        you say "learn async/await patterns for concurrent API calls". Instead
        of "build an app", you say "build a REST API with CRUD endpoints".""",
        allow_delegation=False,
        verbose=True
    )


def create_goals_analysis_task(agent: Agent, project_idea: ProjectIdea, skill_level: str = "intermediate") -> Task:
    """
    Create the task for analyzing goals from a refined project concept.

    Args:
        agent: The GoalsAnalyzerAgent
        project_idea: Refined project concept from ConceptExpanderAgent
        skill_level: User's skill level

    Returns:
        CrewAI Task configured for goals analysis

    Teaching Note:
        Goal extraction is crucial because it drives all downstream decisions:
        - Framework selection picks tools that support these goals
        - Phase design organizes work to achieve these goals
        - Teaching enrichment explains how each step advances these goals

        Good goals are specific, achievable, and aligned with the project.
    """
    description = f"""
Analyze this refined project concept and extract both learning and technical goals:

PROJECT CONCEPT:
{project_idea.refined_summary}

CONSTRAINTS:
{json.dumps(project_idea.constraints, indent=2)}

USER SKILL LEVEL: {skill_level}

Your task is to identify:

1. LEARNING GOALS (2-5 specific goals):
   What concepts, skills, patterns, or paradigms will the user learn?
   - Be specific: "async/await patterns" not "Python"
   - Focus on transferable skills: things that apply beyond this project
   - Match the {skill_level} level: challenging but achievable
   - Mix foundational and advanced concepts appropriately

   Examples of good learning goals:
   - "Understand async/await for concurrent API calls"
   - "Practice component-based UI architecture"
   - "Learn database schema design and migrations"
   - "Master REST API design patterns (CRUD, pagination, filtering)"

2. TECHNICAL GOALS (2-4 specific deliverables):
   What concrete features, components, or capabilities will be built?
   - Be specific: "CRUD API endpoints for user management" not "backend"
   - Focus on core deliverables: what MUST work for the project to succeed?
   - Ensure goals are achievable in the project timeframe

   Examples of good technical goals:
   - "Build a web scraper that handles async requests and rate limiting"
   - "Create an interactive dashboard with real-time data updates"
   - "Implement user authentication with JWT tokens"
   - "Design a multi-agent system with CrewAI for task orchestration"

3. PRIORITY NOTES:
   Brief notes on which goals are most important or time-sensitive.
   What's the core focus? What's nice-to-have vs must-have?

RULES:
- Extract 2-5 learning goals (don't exceed 5)
- Extract 2-4 technical goals (don't exceed 4)
- Be specific and measurable
- Ensure goals align with project concept and constraints
- Goals should be appropriate for {skill_level} level
- Focus on what's realistic given time/complexity constraints

OUTPUT FORMAT (must be valid JSON):
{{
    "learning_goals": [
        "Specific learning goal 1",
        "Specific learning goal 2",
        ...
    ],
    "technical_goals": [
        "Specific technical deliverable 1",
        "Specific technical deliverable 2",
        ...
    ],
    "priority_notes": "Brief statement of what's most important and why"
}}
"""

    return Task(
        description=description,
        expected_output="JSON object with learning_goals, technical_goals, and priority_notes",
        agent=agent
    )


def parse_goals_analysis_result(result: str) -> ProjectGoals:
    """
    Parse the agent's JSON output into a ProjectGoals object.

    Args:
        result: JSON string from the agent

    Returns:
        ProjectGoals with learning and technical objectives

    Teaching Note:
        Same pattern as concept expansion - robust parsing with fallbacks.
        We handle JSON extraction from markdown code blocks and provide
        sensible defaults if parsing fails.
    """
    try:
        # Clean up potential markdown code blocks
        clean_result = result.strip()
        if clean_result.startswith("```"):
            lines = clean_result.split("\n")
            # Remove first and last lines (```json and ```)
            clean_result = "\n".join(lines[1:-1] if len(lines) > 2 else lines)

        data = json.loads(clean_result)

        return ProjectGoals(
            learning_goals=data.get("learning_goals", []),
            technical_goals=data.get("technical_goals", []),
            priority_notes=data.get("priority_notes", "")
        )
    except (json.JSONDecodeError, KeyError, AttributeError) as e:
        print(f"Warning: Could not parse goals analysis output as JSON: {e}")
        print(f"Using fallback goals")

        # Fallback to empty goals (better than crashing)
        return ProjectGoals(
            learning_goals=["Parse error - goals could not be extracted"],
            technical_goals=["Parse error - goals could not be extracted"],
            priority_notes=f"Error parsing goals: {str(e)}"
        )


def analyze_goals(project_idea: ProjectIdea, skill_level: str = "intermediate") -> ProjectGoals:
    """
    High-level function to analyze goals using the GoalsAnalyzerAgent.

    This is the main entry point for goal analysis. It:
    1. Creates the agent
    2. Creates the task with the refined project idea
    3. Executes the task
    4. Parses the result into ProjectGoals

    Args:
        project_idea: Refined concept from ConceptExpanderAgent
        skill_level: User's skill level

    Returns:
        ProjectGoals with learning and technical objectives

    Usage:
        >>> goals = analyze_goals(project_idea, "intermediate")
        >>> print(goals.learning_goals)
        ['Understand async/await patterns', 'Practice API design']
    """
    agent = create_goals_analyzer_agent()
    task = create_goals_analysis_task(agent, project_idea, skill_level)

    # Execute the task
    result = task.execute()

    # Parse into ProjectGoals
    project_goals = parse_goals_analysis_result(result)

    return project_goals
