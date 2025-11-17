"""
ConceptExpanderAgent - Transforms raw project ideas into structured concepts.

This agent is the first in the Project Forge pipeline. It receives messy, vague
user input like "build something with Streamlit" and expands it into a clear,
structured ProjectIdea with refined summary and constraints.

Key responsibilities:
- Clean and normalize raw text input
- Identify implicit constraints (time, complexity, scope)
- Expand vague ideas into concrete, actionable concepts
- Remove ambiguity while preserving user intent

The output ProjectIdea becomes the foundation for all downstream agents
(GoalsAnalyzer, FrameworkSelector, PhaseDesigner, etc.).
"""

from crewai import Agent, Task
from typing import Dict, Any
import json

from ..models.project_models import ProjectIdea
from ..tools.text_cleaner_tool import clean_project_idea, extract_keywords


def create_concept_expander_agent() -> Agent:
    """
    Create the ConceptExpanderAgent with specialized prompting for idea expansion.

    This agent uses an LLM to take cleaned user input and expand it into a
    comprehensive project concept. It infers missing details, identifies constraints,
    and creates a solid foundation for planning.

    Returns:
        CrewAI Agent configured for concept expansion

    Teaching Note:
        CrewAI agents are defined by role, goal, and backstory. The backstory
        shapes the agent's "personality" and decision-making style. This agent
        is designed to be thorough but not overly prescriptive - it expands
        ideas while staying true to user intent.
    """
    return Agent(
        role="Project Concept Expander",
        goal="Transform raw, vague project ideas into clear, structured, and actionable concepts",
        backstory="""You are an expert product strategist and technical architect
        who excels at taking half-formed ideas and turning them into crystal-clear
        project concepts.

        You have a gift for:
        - Understanding what users really mean, even when they're vague
        - Identifying implied constraints (time, skill, complexity, resources)
        - Expanding ideas with just enough detail to be actionable
        - Preserving the user's original vision while removing ambiguity
        - Recognizing when a project is too big or too small and adjusting scope

        You DO NOT make wild assumptions or add features the user didn't ask for.
        You clarify, structure, and enhance - but always stay grounded in the
        user's actual intent.""",
        allow_delegation=False,
        verbose=True
    )


def create_concept_expansion_task(agent: Agent, raw_idea: str, skill_level: str = "intermediate") -> Task:
    """
    Create the task for expanding a raw idea into a ProjectIdea.

    This task provides the agent with the raw input and asks it to produce
    a structured JSON output that we can parse into a ProjectIdea object.

    Args:
        agent: The ConceptExpanderAgent
        raw_idea: Raw user input from CLI
        skill_level: User's skill level (beginner/intermediate/advanced)

    Returns:
        CrewAI Task configured for concept expansion

    Teaching Note:
        Tasks in CrewAI define WHAT to do. They include:
        - description: the actual prompt/instructions
        - expected_output: what format the result should be in
        - agent: which agent executes this task

        The description is the key - it's where we encode domain knowledge
        and guide the LLM's reasoning process.
    """
    # Pre-clean the raw idea using our text cleaning tools
    cleaned_idea = clean_project_idea(raw_idea)
    keywords = extract_keywords(cleaned_idea)

    description = f"""
Take this raw project idea and expand it into a clear, structured concept:

RAW IDEA: "{cleaned_idea}"
USER SKILL LEVEL: {skill_level}
EXTRACTED KEYWORDS: {', '.join(keywords)}

Your task is to create a comprehensive project concept with these components:

1. REFINED SUMMARY (2-4 sentences):
   - Clear statement of what will be built
   - Core functionality and purpose
   - Key features or capabilities
   - Target outcome or deliverable

2. CONSTRAINTS (identify and articulate):
   - Time: How long should this realistically take? (e.g., "1 week", "2-3 weeks")
   - Complexity: What's the appropriate complexity level? ("low", "medium", "high")
   - Scope: What's in vs out of scope?
   - Technical: Any technical limitations or requirements?
   - Skill: Is this appropriate for the user's {skill_level} skill level?

RULES:
- Be specific but not overly prescriptive
- Infer reasonable constraints from the idea
- For {skill_level} users, suggest appropriate scope
- Preserve the user's original intent - don't add features they didn't want
- If the idea is too vague, make reasonable assumptions but note them
- If the idea seems too ambitious for the skill level, suggest a reasonable subset

OUTPUT FORMAT (must be valid JSON):
{{
    "refined_summary": "Clear 2-4 sentence description of the project...",
    "constraints": {{
        "time": "1-2 weeks",
        "complexity": "medium",
        "scope": "Brief scope statement",
        "technical_requirements": "Any specific tech requirements",
        "skill_appropriateness": "Why this fits {skill_level} level"
    }}
}}
"""

    return Task(
        description=description,
        expected_output="JSON object with refined_summary and constraints dict",
        agent=agent
    )


def parse_concept_expansion_result(result: str, raw_idea: str) -> ProjectIdea:
    """
    Parse the agent's JSON output into a ProjectIdea object.

    Args:
        result: JSON string from the agent
        raw_idea: Original raw input (for fallback)

    Returns:
        ProjectIdea with refined summary and constraints

    Teaching Note:
        LLM outputs can be unpredictable, so we need robust parsing with
        fallbacks. This function tries to extract JSON, handles errors
        gracefully, and ensures we always return a valid ProjectIdea even
        if the agent's output was malformed.
    """
    try:
        # Try to parse as JSON
        # The LLM might wrap JSON in markdown code blocks, so strip those
        clean_result = result.strip()
        if clean_result.startswith("```"):
            # Extract content between ``` markers
            lines = clean_result.split("\n")
            clean_result = "\n".join(lines[1:-1])

        data = json.loads(clean_result)

        return ProjectIdea(
            raw_description=raw_idea,
            refined_summary=data.get("refined_summary", raw_idea),
            constraints=data.get("constraints", {})
        )
    except (json.JSONDecodeError, KeyError, AttributeError) as e:
        # Fallback: if JSON parsing fails, use the raw output as refined summary
        print(f"Warning: Could not parse agent output as JSON: {e}")
        print(f"Using raw output as refined summary")

        return ProjectIdea(
            raw_description=raw_idea,
            refined_summary=result.strip(),
            constraints={"parsing_error": str(e)}
        )


def expand_concept(raw_idea: str, skill_level: str = "intermediate") -> ProjectIdea:
    """
    High-level function to expand a raw idea using the ConceptExpanderAgent.

    This is the main entry point for concept expansion. It:
    1. Creates the agent
    2. Creates the task
    3. Executes the task
    4. Parses the result into a ProjectIdea

    Args:
        raw_idea: Raw project idea from user
        skill_level: User's skill level

    Returns:
        ProjectIdea with refined concept and constraints

    Usage:
        >>> idea = expand_concept("build a streamlit dashboard", "beginner")
        >>> print(idea.refined_summary)
        "A Streamlit web application that visualizes data in an interactive dashboard..."
    """
    agent = create_concept_expander_agent()
    task = create_concept_expansion_task(agent, raw_idea, skill_level)

    # Execute the task (CrewAI will call the LLM)
    result = task.execute()

    # Parse into ProjectIdea
    project_idea = parse_concept_expansion_result(result, raw_idea)

    return project_idea
