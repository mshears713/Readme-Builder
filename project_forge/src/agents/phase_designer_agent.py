"""
PhaseDesignerAgent - Structures projects into 5 phases with ~10 steps each.

This agent takes the refined project concept, goals, and framework choices and
creates a detailed 5-phase build plan with approximately 50 total steps. Each
step is small, concrete, and buildable in a single focused session.

Key responsibilities:
- Break the project into 5 logical phases
- Create ~10 concrete, actionable steps per phase
- Ensure steps are small enough (30-90 minutes each)
- Maintain proper dependencies between steps
- Keep steps focused on building, not just research

The output Phase objects will be enriched by TeacherAgent with pedagogical
annotations before final README generation.

Teaching Note:
    This is where we transform a vision into a structured build plan. The key
    challenge is finding the right granularity - steps that are small enough
    to feel achievable but substantial enough to make meaningful progress.

    We follow the "5 phases × 10 steps" structure because:
    - 5 phases create natural milestones and breaks
    - ~10 steps per phase is digestible and trackable
    - 50 total steps typically maps to 1-4 weeks of focused work
    - This structure makes progress visible and momentum sustainable
"""

from crewai import Agent, Task
from typing import List, Dict, Any
import json

from ..models.project_models import ProjectIdea, ProjectGoals, FrameworkChoice, Phase, Step


def create_phase_designer_agent() -> Agent:
    """
    Create the PhaseDesignerAgent with specialized prompting for build planning.

    This agent understands how to structure projects into logical phases and
    break those phases into small, concrete steps. It has strong intuitions
    about appropriate scope and realistic timeframes.

    Returns:
        CrewAI Agent configured for phase design

    Teaching Note:
        The backstory shapes how this agent thinks about project structure.
        We want it to be pragmatic, realistic about scope, and focused on
        concrete deliverables rather than vague "research" or "learn" steps.
    """
    return Agent(
        role="Project Phase Designer",
        goal="Transform project concepts into structured 5-phase build plans with ~50 concrete, actionable steps",
        backstory="""You are an expert project architect and engineering manager
        who excels at breaking complex projects into manageable phases and steps.

        You have decades of experience:
        - Structuring projects into logical, progressive phases
        - Breaking phases into small, concrete steps (30-90 minutes each)
        - Ensuring steps build on each other naturally
        - Avoiding "research" or "learn" steps - every step produces something
        - Keeping scope realistic and achievable
        - Creating clear milestones and progress markers

        Your philosophy:
        - Small steps create momentum and confidence
        - Every step should have a tangible deliverable
        - Dependencies should be clear and minimal
        - Early phases focus on foundations, later phases on features and polish
        - Each phase should end with something working

        You DO NOT:
        - Create vague steps like "research X" or "learn about Y"
        - Make steps too large (multi-hour or multi-day efforts)
        - Ignore dependencies or assume knowledge appears magically
        - Front-load all the hard work or back-load all the easy work
        - Create more than 5 phases or wildly unbalanced phase sizes""",
        allow_delegation=False,
        verbose=True
    )


def create_phase_design_task(
    agent: Agent,
    idea: ProjectIdea,
    goals: ProjectGoals,
    framework: FrameworkChoice,
    skill_level: str = "intermediate"
) -> Task:
    """
    Create the task for designing phases and steps.

    This task provides comprehensive context about the project and asks the
    agent to produce a structured 5-phase plan with detailed steps.

    Args:
        agent: The PhaseDesignerAgent
        idea: Refined project concept with constraints
        goals: Learning and technical objectives
        framework: Selected technology stack
        skill_level: User's skill level

    Returns:
        CrewAI Task configured for phase design

    Teaching Note:
        The prompt is quite detailed because we need to guide the LLM to
        produce a very specific structure. We provide rules, examples, and
        format specifications to minimize ambiguity and maximize quality.
    """
    description = f"""
Create a detailed 5-phase build plan for this project:

PROJECT CONCEPT:
{idea.refined_summary}

CONSTRAINTS:
{json.dumps(idea.constraints, indent=2)}

LEARNING GOALS:
{chr(10).join(f'- {goal}' for goal in goals.learning_goals)}

TECHNICAL GOALS:
{chr(10).join(f'- {goal}' for goal in goals.technical_goals)}

SELECTED FRAMEWORKS:
- Frontend: {framework.frontend or 'None (CLI-only)'}
- Backend: {framework.backend or 'None'}
- Storage: {framework.storage or 'None'}
- Libraries: {', '.join(framework.special_libs) if framework.special_libs else 'Standard libs'}

USER SKILL LEVEL: {skill_level}

Your task is to create a 5-phase build plan with approximately 10 steps per phase (50 total).

PHASE STRUCTURE GUIDELINES:
Phase 1 should typically cover: foundations, setup, data models, basic structure
Phase 2 should typically cover: core functionality, main features, basic integration
Phase 3 should typically cover: additional features, refinements, edge cases
Phase 4 should typically cover: polish, testing, error handling, optimization
Phase 5 should typically cover: documentation, examples, final touches, deployment prep

STEP REQUIREMENTS:
1. Each step should take 30-90 minutes to complete
2. Each step must be concrete and actionable (not "learn X" or "research Y")
3. Each step must produce a tangible output (code, file, feature, etc.)
4. Steps should build on previous steps naturally
5. Dependencies should be minimal and clear
6. Use specific technical terms matching the chosen frameworks
7. Steps should match the {skill_level} skill level

WHAT MAKES A GOOD STEP:
✓ "Create User dataclass with email, password_hash, and created_at fields"
✓ "Implement login endpoint in FastAPI with POST /auth/login"
✓ "Add SQLite table creation for users with migrations"
✓ "Build Streamlit form for user input with validation"

WHAT MAKES A BAD STEP:
✗ "Learn about authentication" (too vague, not actionable)
✗ "Build the entire API" (too large, not a single step)
✗ "Research best practices" (no deliverable)
✗ "Make it work" (not specific)

OUTPUT FORMAT (must be valid JSON):
{{
    "phases": [
        {{
            "index": 1,
            "name": "Phase Name (e.g., Foundations & Setup)",
            "description": "1-2 sentence overview of what this phase accomplishes",
            "steps": [
                {{
                    "index": 1,
                    "title": "Short, specific step name",
                    "description": "Detailed instructions for this step (2-4 sentences). Be specific about what to build, which files to create/modify, and what the deliverable looks like.",
                    "dependencies": []
                }},
                ... (approximately 10 steps per phase)
            ]
        }},
        ... (5 phases total)
    ]
}}

IMPORTANT:
- Generate exactly 5 phases
- Aim for approximately 10 steps per phase (can be 8-12 per phase, totaling ~50)
- Number steps globally from 1-50 (not resetting per phase)
- Only include dependencies when truly necessary (step N depends on step M)
- Make every step concrete and buildable
- Ensure progressive difficulty appropriate for {skill_level} users
"""

    return Task(
        description=description,
        expected_output="JSON object with 5 phases containing approximately 50 total steps",
        agent=agent
    )


def parse_phase_design_result(result: str) -> List[Phase]:
    """
    Parse the agent's JSON output into Phase and Step objects.

    Args:
        result: JSON string from the agent containing phases and steps

    Returns:
        List of Phase objects with populated Step lists

    Teaching Note:
        JSON parsing from LLM outputs requires defensive coding. We handle:
        - Markdown code blocks wrapping the JSON
        - Missing or malformed fields
        - Incorrect numbering
        - Empty or missing steps

        We also validate and fix step numbering to ensure global sequential
        indices, since the LLM might reset numbering per phase.
    """
    try:
        # Clean up markdown code blocks if present
        clean_result = result.strip()
        if clean_result.startswith("```"):
            lines = clean_result.split("\n")
            # Remove first and last lines (```json and ```)
            clean_result = "\n".join(lines[1:-1])

        data = json.loads(clean_result)
        phases_data = data.get("phases", [])

        if not phases_data:
            raise ValueError("No phases found in agent output")

        phases = []
        global_step_index = 1  # Track global step numbering

        for phase_data in phases_data:
            steps = []
            steps_data = phase_data.get("steps", [])

            for step_data in steps_data:
                # Fix step index to be global rather than per-phase
                step = Step(
                    index=global_step_index,
                    title=step_data.get("title", f"Step {global_step_index}"),
                    description=step_data.get("description", ""),
                    what_you_learn="",  # Will be filled by TeacherAgent
                    dependencies=step_data.get("dependencies", [])
                )
                steps.append(step)
                global_step_index += 1

            phase = Phase(
                index=phase_data.get("index", len(phases) + 1),
                name=phase_data.get("name", f"Phase {len(phases) + 1}"),
                description=phase_data.get("description", ""),
                steps=steps
            )
            phases.append(phase)

        return phases

    except (json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"Error parsing phase design result: {e}")
        print(f"Raw result: {result[:500]}...")

        # Return a minimal fallback structure
        return [
            Phase(
                index=1,
                name="Phase 1: Setup (Parsing Error)",
                description=f"Error parsing plan: {str(e)}",
                steps=[
                    Step(
                        index=1,
                        title="Fix phase design parsing",
                        description="The agent output could not be parsed. Check the raw output and fix the JSON structure.",
                        what_you_learn="",
                        dependencies=[]
                    )
                ]
            )
        ]


def design_phases(
    idea: ProjectIdea,
    goals: ProjectGoals,
    framework: FrameworkChoice,
    skill_level: str = "intermediate"
) -> List[Phase]:
    """
    High-level function to design project phases using PhaseDesignerAgent.

    This is the main entry point for phase design. It:
    1. Creates the agent
    2. Creates the task with full context
    3. Executes the task
    4. Parses the result into Phase/Step objects

    Args:
        idea: Refined project concept
        goals: Learning and technical objectives
        framework: Selected technology stack
        skill_level: User's skill level

    Returns:
        List of 5 Phase objects with ~50 total steps

    Usage:
        >>> phases = design_phases(idea, goals, framework, "intermediate")
        >>> print(f"Created {len(phases)} phases with {sum(len(p.steps) for p in phases)} total steps")
        Created 5 phases with 50 total steps
    """
    agent = create_phase_designer_agent()
    task = create_phase_design_task(agent, idea, goals, framework, skill_level)

    # Execute the task
    result = task.execute()

    # Parse into Phase objects
    phases = parse_phase_design_result(result)

    return phases
