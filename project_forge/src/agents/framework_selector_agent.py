"""
FrameworkSelectorAgent - Chooses appropriate technology stacks for projects.

This agent is the third in the Project Forge pipeline. It receives a refined
ProjectIdea and ProjectGoals, then selects appropriate frameworks, libraries,
and tools that match the user's skill level and project requirements.

Key responsibilities:
- Choose frontend frameworks (Streamlit, React, Flask, or CLI-only)
- Choose backend frameworks (FastAPI, Flask, Django, or scripts)
- Choose storage solutions (SQLite, PostgreSQL, JSON files, etc.)
- Select domain-specific libraries (CrewAI, LangChain, BeautifulSoup, etc.)
- Balance simplicity, learning value, and project needs
- Avoid bleeding-edge or overly complex tools for beginners

The output FrameworkChoice guides the build plan and teaching approach.
"""

from crewai import Agent, Task
from typing import Dict, Any
import json
import yaml
from pathlib import Path

from ..models.project_models import ProjectIdea, ProjectGoals, FrameworkChoice


def load_framework_config() -> Dict[str, Any]:
    """
    Load framework templates and skill level presets from defaults.yaml.

    Returns:
        Dict with skill_levels and framework_templates

    Teaching Note:
        Externalizing configuration to YAML makes the system flexible and
        maintainable. Users can edit defaults.yaml to add new framework
        templates or adjust skill level recommendations without touching code.
    """
    config_path = Path(__file__).parent.parent / "config" / "defaults.yaml"
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        print(f"Warning: Could not load config from {config_path}: {e}")
        # Return minimal fallback config
        return {
            "skill_levels": {},
            "framework_templates": {}
        }


def create_framework_selector_agent() -> Agent:
    """
    Create the FrameworkSelectorAgent with specialized prompting for tech stack selection.

    This agent acts as a pragmatic tech lead who knows when to use simple
    tools vs. complex ones. It prioritizes developer experience, learning
    value, and well-documented, stable technologies.

    Returns:
        CrewAI Agent configured for framework selection

    Teaching Note:
        Framework selection is a crucial educational moment. The wrong choice
        can lead to frustration (too complex) or boredom (too simple). This
        agent tries to hit the "Goldilocks zone" - just right for the user's
        skill level and project needs.
    """
    return Agent(
        role="Technology Stack Advisor",
        goal="Select appropriate, well-matched frameworks and tools for the project",
        backstory="""You are a pragmatic tech lead with deep knowledge of
        modern frameworks, libraries, and tools across multiple languages and
        domains.

        Your philosophy:
        - Simple is better than complex
        - Well-documented is better than cutting-edge
        - Learning value matters as much as technical capability
        - Match tools to skill level: don't overwhelm beginners, don't bore experts
        - Prefer popular, stable tools with good community support
        - Avoid over-engineering: use the simplest tool that meets the need

        You have expertise in:
        - Frontend: Streamlit, Gradio, React, Vue, Flask+Jinja, CLI-only apps
        - Backend: FastAPI, Flask, Django, Express, simple Python scripts
        - Storage: SQLite, PostgreSQL, MongoDB, Redis, JSON files, CSV
        - AI/ML: CrewAI, LangChain, OpenAI API, Hugging Face
        - Web scraping: BeautifulSoup, Scrapy, httpx, aiohttp
        - Data: pandas, numpy, matplotlib, plotly

        You always consider:
        - Developer experience (DX): Is this easy to learn and use?
        - Documentation: Can the user find help when stuck?
        - Ecosystem: Are there good tutorials, examples, and libraries?
        - Deployment: How hard is it to run and deploy?

        You're not afraid to recommend "boring" technology if it's the right
        choice. Sometimes SQLite beats PostgreSQL, and that's okay.""",
        allow_delegation=False,
        verbose=True
    )


def create_framework_selection_task(
    agent: Agent,
    project_idea: ProjectIdea,
    project_goals: ProjectGoals,
    skill_level: str = "intermediate"
) -> Task:
    """
    Create the task for selecting frameworks and tools.

    Args:
        agent: The FrameworkSelectorAgent
        project_idea: Refined project concept
        project_goals: Learning and technical goals
        skill_level: User's skill level

    Returns:
        CrewAI Task configured for framework selection

    Teaching Note:
        This task provides the agent with rich context (idea, goals, skill level,
        and framework templates from config). The agent uses all this information
        to make informed recommendations that balance learning value, simplicity,
        and project requirements.
    """
    # Load configuration for framework templates and skill level guidance
    config = load_framework_config()
    skill_config = config.get("skill_levels", {}).get(skill_level, {})
    framework_templates = config.get("framework_templates", {})

    description = f"""
Select appropriate frameworks and tools for this project:

PROJECT CONCEPT:
{project_idea.refined_summary}

LEARNING GOALS:
{chr(10).join(f"- {goal}" for goal in project_goals.learning_goals)}

TECHNICAL GOALS:
{chr(10).join(f"- {goal}" for goal in project_goals.technical_goals)}

USER SKILL LEVEL: {skill_level}
SKILL LEVEL GUIDANCE:
{json.dumps(skill_config, indent=2)}

AVAILABLE FRAMEWORK TEMPLATES:
{json.dumps(framework_templates, indent=2)}

Your task is to select:

1. FRONTEND (or None if CLI-only):
   - Streamlit: Great for quick data apps, dashboards, prototypes (beginner-friendly)
   - Gradio: Best for ML/AI demos and interfaces (beginner-friendly)
   - Flask + Jinja: Simple server-rendered web apps (intermediate)
   - React: Modern frontend for complex UIs (intermediate-advanced)
   - Vue/Svelte: Alternative to React, slightly simpler (intermediate)
   - None: For CLI tools, APIs, background services

2. BACKEND (or None if frontend handles everything):
   - FastAPI: Modern, fast, great for APIs and async (intermediate)
   - Flask: Simple, flexible, good for small-medium apps (beginner-intermediate)
   - Django: Full-featured, best for larger apps with auth/admin (advanced)
   - CLI-only: For command-line tools, scripts (any level)
   - Python scripts: For automation, data processing (beginner)

3. STORAGE:
   - JSON files: Simplest, good for small data (beginner)
   - CSV files: Good for tabular data (beginner)
   - SQLite: Great starter database, no setup needed (beginner-intermediate)
   - PostgreSQL: Robust, production-ready (intermediate-advanced)
   - MongoDB: NoSQL, flexible schemas (intermediate)
   - Redis: In-memory, caching, real-time (advanced)

4. SPECIAL LIBRARIES (domain-specific):
   Based on the project goals, what specialized libraries are needed?
   - AI/Agents: crewai, langchain, openai
   - Web scraping: beautifulsoup4, scrapy, httpx, aiohttp
   - Data science: pandas, numpy, matplotlib, plotly
   - Testing: pytest, unittest
   - Other domain-specific tools

SELECTION CRITERIA:
- Match skill level: don't overwhelm {skill_level} users
- Prioritize simplicity and good documentation
- Choose well-established tools with strong communities
- Ensure tools support the learning and technical goals
- Consider development speed and ease of deployment
- Avoid unnecessary complexity

OUTPUT FORMAT (must be valid JSON):
{{
    "frontend": "Streamlit" or null,
    "backend": "FastAPI" or "CLI-only" or null,
    "storage": "SQLite",
    "special_libs": ["crewai", "openai", "pandas"],
    "rationale": "Brief explanation of why these choices fit the project and skill level"
}}
"""

    return Task(
        description=description,
        expected_output="JSON object with frontend, backend, storage, special_libs, and rationale",
        agent=agent
    )


def parse_framework_selection_result(result: str) -> FrameworkChoice:
    """
    Parse the agent's JSON output into a FrameworkChoice object.

    Args:
        result: JSON string from the agent

    Returns:
        FrameworkChoice with selected frameworks and libraries

    Teaching Note:
        Framework selection output includes a rationale field that's useful
        for debugging and understanding the agent's reasoning, but we don't
        store it in the FrameworkChoice model. We print it for visibility
        during execution.
    """
    try:
        # Clean up potential markdown code blocks
        clean_result = result.strip()
        if clean_result.startswith("```"):
            lines = clean_result.split("\n")
            clean_result = "\n".join(lines[1:-1] if len(lines) > 2 else lines)

        data = json.loads(clean_result)

        # Print rationale if provided (helpful for debugging)
        if "rationale" in data:
            print(f"\nFramework Selection Rationale:")
            print(f"  {data['rationale']}\n")

        return FrameworkChoice(
            frontend=data.get("frontend"),
            backend=data.get("backend"),
            storage=data.get("storage"),
            special_libs=data.get("special_libs", [])
        )
    except (json.JSONDecodeError, KeyError, AttributeError) as e:
        print(f"Warning: Could not parse framework selection output as JSON: {e}")
        print(f"Using fallback framework choices")

        # Fallback to safe defaults
        return FrameworkChoice(
            frontend="Streamlit",
            backend="Python",
            storage="JSON files",
            special_libs=[]
        )


def select_frameworks(
    project_idea: ProjectIdea,
    project_goals: ProjectGoals,
    skill_level: str = "intermediate"
) -> FrameworkChoice:
    """
    High-level function to select frameworks using the FrameworkSelectorAgent.

    This is the main entry point for framework selection. It:
    1. Creates the agent
    2. Creates the task with project context
    3. Executes the task
    4. Parses the result into FrameworkChoice

    Args:
        project_idea: Refined project concept
        project_goals: Learning and technical goals
        skill_level: User's skill level

    Returns:
        FrameworkChoice with selected tech stack

    Usage:
        >>> frameworks = select_frameworks(idea, goals, "beginner")
        >>> print(f"Frontend: {frameworks.frontend}, Backend: {frameworks.backend}")
        Frontend: Streamlit, Backend: Python
    """
    agent = create_framework_selector_agent()
    task = create_framework_selection_task(agent, project_idea, project_goals, skill_level)

    # Execute the task
    result = task.execute()

    # Parse into FrameworkChoice
    framework_choice = parse_framework_selection_result(result)

    return framework_choice
