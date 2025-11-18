"""
TeacherAgent - Adds comprehensive implementation guidance for autonomous AI execution.

This agent takes the structured phase/step plan from PhaseDesignerAgent and
enriches it with detailed implementation guidance. It adds "teaching_guidance"
fields to each step that provide comprehensive technical details, code patterns,
and architectural guidance that AI agents need for autonomous execution.

Key responsibilities:
- Add detailed "teaching_guidance" to each step for AI execution
- Specify exact implementation patterns, code structures, and technical approaches
- Provide comprehensive details so AI agents can execute without clarification
- Include specific file names, function signatures, and technical decisions
- Ensure steps are complete enough for 1+ hour autonomous execution
- Guide the AI on what code, documentation, and features to implement

The output is an enriched ProjectPlan where every step includes comprehensive
implementation details that enable autonomous AI execution without user intervention.

Teaching Note:
    This agent now focuses on IMPLEMENTATION GUIDANCE for AI agents rather than
    educational features for end users. The guidance should be so detailed and
    clear that an AI agent can execute the step completely autonomously.

    Good implementation guidance:
    - Specifies exact code patterns and technical approaches
    - Includes file names, function signatures, and architectural decisions
    - Provides enough detail that no external research is needed
    - Mentions any documentation or comments to include in the code
    - Ensures the AI can build a complete, working feature autonomously
"""

from crewai import Agent, Task
from typing import List, Dict, Any
import json

from ..models.project_models import ProjectIdea, ProjectGoals, Phase, Step, ProjectPlan


def create_teacher_agent() -> Agent:
    """
    Create the TeacherAgent that provides comprehensive implementation guidance for AI execution.

    This agent specializes in enriching build steps with detailed technical guidance
    that enables autonomous AI execution. It provides the missing implementation
    details that allow AI agents to complete steps without clarification or research.

    Returns:
        CrewAI Agent configured for implementation guidance

    Teaching Note:
        This agent provides IMPLEMENTATION GUIDANCE for the executing AI agent,
        not educational features for end users. It fills in technical details,
        code patterns, and architectural decisions so the AI can work autonomously.
    """
    return Agent(
        role="Technical Implementation Guide and Software Architecture Specialist",
        goal="Provide comprehensive implementation guidance that enables AI agents to execute build steps autonomously",
        backstory="""You are an expert software architect and technical mentor who
        specializes in providing detailed implementation guidance for AI agents.
        Your role is to enrich high-level build steps with the technical details
        needed for autonomous execution.

        Your expertise includes:
        - Specifying exact code patterns and architectural approaches
        - Providing comprehensive technical details for autonomous implementation
        - Defining file structures, function signatures, and data models
        - Explaining technical decisions and rationale
        - Detailing error handling, edge cases, and robustness requirements
        - Specifying what documentation and comments to include in code
        - Ensuring no ambiguity that would require external research
        - Making implementation steps self-contained and complete

        Your philosophy for AI-executable guidance:
        - Every step should be implementable without clarification
        - Technical details should be specific and unambiguous
        - Code patterns and structures should be explicitly stated
        - File names, function names, and key APIs should be mentioned
        - The AI should never need to stop and ask for more information
        - Implementation guidance is comprehensive, not minimal
        - Good guidance enables 1+ hours of autonomous work

        You provide guidance that tells the implementing AI:
        - What specific code patterns and structures to use
        - Which files to create/modify and what to put in them
        - What function signatures and class definitions to implement
        - How to handle errors and edge cases
        - What comments and docstrings to include for code clarity
        - What testing or validation to perform
        - Any configuration or setup requirements
        - Architectural decisions and technical rationale
        - What user-facing documentation or help features to add (if applicable)

        You DO NOT:
        - Write vague suggestions like "implement appropriately"
        - Leave technical decisions ambiguous or unspecified
        - Assume the AI will figure out missing details
        - Focus on theory without practical implementation guidance
        - Create guidance that requires external research or clarification""",
        allow_delegation=False,
        verbose=True
    )


def create_teaching_enrichment_task(
    agent: Agent,
    phases: List[Phase],
    goals: ProjectGoals,
    skill_level: str = "intermediate"
) -> Task:
    """
    Create the task for adding comprehensive implementation guidance to phases and steps.

    This task provides the existing phase structure and asks the agent to
    enrich each step with detailed technical guidance for autonomous AI execution.

    Args:
        agent: The TeacherAgent (now an implementation guidance specialist)
        phases: List of Phase objects from PhaseDesignerAgent (steps have empty teaching_guidance)
        goals: Learning and technical objectives for context
        skill_level: Skill level of the final program's users

    Returns:
        CrewAI Task configured for implementation guidance enrichment

    Teaching Note:
        We pass the full phase structure to the agent and ask it to return
        the same structure with added implementation guidance. This preserves
        the step details while adding comprehensive technical details for AI execution.
    """
    # Build a summary of the phases for context
    phases_summary = []
    for phase in phases:
        steps_summary = [f"  {s.index}. {s.title}" for s in phase.steps]
        phases_summary.append(
            f"Phase {phase.index}: {phase.name}\n" + "\n".join(steps_summary)
        )

    description = f"""
Add comprehensive implementation guidance to enable AUTONOMOUS AI EXECUTION of this project plan.

CRITICAL: This plan will be executed by an AI agent (like Claude Code) that will complete
ALL steps in ONE CONTINUOUS SESSION without user intervention. Your guidance must be detailed
enough that the AI can work autonomously for 1+ hours and deliver a complete, working project.

LEARNING GOALS (what users should learn from using the final program):
{chr(10).join(f'- {goal}' for goal in goals.learning_goals)}

TECHNICAL GOALS (what the program must do):
{chr(10).join(f'- {goal}' for goal in goals.technical_goals)}

TARGET USER SKILL LEVEL: {skill_level}

CURRENT PLAN STRUCTURE:
{chr(10).join(phases_summary)}

Your task is to:
1. Add comprehensive "teaching_guidance" to EVERY step (detailed implementation guidance)
2. Create global implementation notes for the AI agent's overall strategy

CRITICAL: You are providing IMPLEMENTATION GUIDANCE for the AI agent, not educational
features for end users. Your guidance should enable autonomous execution without clarification.

GUIDELINES FOR "teaching_guidance" IMPLEMENTATION DETAILS:
- Write 2-5 sentences of comprehensive technical guidance
- Specify exact code patterns, file names, and technical approaches
- Include function signatures, class definitions, or key algorithms
- Mention error handling and edge cases to consider
- Specify what comments/docstrings to include in the code
- Tell the AI what to implement, how to structure it, and where to put it
- Be specific enough that no external research or clarification is needed
- Include any user-facing documentation or help features to build (if applicable)
- Ensure the guidance is complete and unambiguous

EXAMPLES OF GOOD IMPLEMENTATION GUIDANCE:
✓ "Create a User dataclass in models/user.py with fields: email (str), password_hash (str), created_at (datetime). Use bcrypt for password hashing. Include docstring explaining the user model and add a validate_email() method with regex checking. Add inline comments explaining the hashing approach."

✓ "Implement POST /auth/login in routes/auth.py using FastAPI. Accept email/password in request body, query database for user, verify password with bcrypt.checkpw(), return JWT token on success or 401 on failure. Include proper error handling and logging. Add docstring with example request/response."

✓ "Create database.py with SQLite connection using sqlite3. Define init_db() function that creates users table with schema: id INTEGER PRIMARY KEY, email TEXT UNIQUE, password_hash TEXT, created_at TIMESTAMP. Use context manager for connections. Add comprehensive comments explaining connection pooling and thread safety."

✓ "Build a Streamlit login form in pages/login.py with st.text_input for email/password and st.button for submit. On submit, call auth API and handle response. Display st.success() or st.error() based on result. Include st.help() tooltip explaining the authentication flow. Add error messages for invalid inputs."

EXAMPLES OF BAD IMPLEMENTATION GUIDANCE:
✗ "Set up the database appropriately" (too vague, no specific guidance)
✗ "Add user authentication" (not specific about how or what to implement)
✗ "Handle errors as needed" (ambiguous, AI doesn't know which errors)
✗ "Create API endpoints" (which endpoints? what should they do?)
✗ "Make it secure" (not actionable without specific guidance)
✗ "Research best practices and implement" (requires external research)

GUIDELINES FOR GLOBAL IMPLEMENTATION NOTES:
- Write 4-7 sentences instructing the AI on overall implementation strategy
- Specify overarching architectural patterns and technical approaches
- Describe how components should integrate and interact
- Mention testing strategy and code quality expectations
- Emphasize that code should be complete and production-ready (no TODOs or stubs)
- Remind the AI to work sequentially and autonomously through all steps
- Note any user-facing documentation or educational features to build into the program

OUTPUT FORMAT (must be valid JSON):
{{
    "enriched_phases": [
        {{
            "index": 1,
            "name": "Phase name from input",
            "description": "Phase description from input",
            "steps": [
                {{
                    "index": 1,
                    "title": "Step title from input",
                    "description": "Step description from input",
                    "teaching_guidance": "YOUR COMPREHENSIVE IMPLEMENTATION GUIDANCE HERE (2-5 sentences with specific technical details, file names, code patterns, error handling, and documentation requirements)",
                    "dependencies": []
                }},
                ...
            ]
        }},
        ...
    ],
    "global_teaching_notes": "Your 4-7 sentence overview of the implementation strategy, architectural patterns, testing approach, and autonomous execution guidelines for the AI agent to follow..."
}}

IMPORTANT FOR AUTONOMOUS EXECUTION:
- Preserve all existing step data (title, description, dependencies, indices)
- Only ADD the "teaching_guidance" field and global_teaching_notes
- Write comprehensive guidance for ALL {sum(len(p.steps) for p in phases)} steps
- Make each guidance specific, detailed, and unambiguous for that step
- Include enough technical detail that the AI needs no clarification
- Ensure the AI can execute all steps sequentially without stopping
- Remember: You're providing IMPLEMENTATION DETAILS for autonomous AI execution
- The final program should be appropriate for {skill_level} users
"""

    return Task(
        description=description,
        expected_output="""JSON object with enriched phases (including comprehensive implementation
        guidance in teaching_guidance for all steps) and global implementation notes. Each
        teaching_guidance must provide detailed technical guidance (2-5 sentences) with specific
        code patterns, file names, function signatures, error handling, and documentation
        requirements that enable autonomous AI execution without clarification.""",
        agent=agent
    )


def parse_teaching_enrichment_result(result: str, original_phases: List[Phase]) -> tuple[List[Phase], str]:
    """
    Parse the agent's JSON output and merge teaching annotations into Phase/Step objects.

    Args:
        result: JSON string from the agent with enriched phases
        original_phases: Original phases to use as fallback

    Returns:
        Tuple of (enriched phases, global teaching notes)

    Teaching Note:
        We merge the agent's teaching annotations into our existing Phase/Step
        objects rather than replacing them entirely. This ensures we preserve
        all the original data and only add the teaching fields.
    """
    try:
        # Clean up markdown code blocks
        clean_result = result.strip()
        if clean_result.startswith("```"):
            lines = clean_result.split("\n")
            clean_result = "\n".join(lines[1:-1])

        data = json.loads(clean_result)
        enriched_phases_data = data.get("enriched_phases", [])
        global_notes = data.get("global_teaching_notes", "")

        # Create enriched phases by merging with original data
        enriched_phases = []

        for phase_idx, phase_data in enumerate(enriched_phases_data):
            # Get original phase as fallback
            original_phase = original_phases[phase_idx] if phase_idx < len(original_phases) else None

            steps = []
            steps_data = phase_data.get("steps", [])

            for step_idx, step_data in enumerate(steps_data):
                # Get original step as fallback
                original_step = None
                if original_phase and step_idx < len(original_phase.steps):
                    original_step = original_phase.steps[step_idx]

                # Create enriched step, preserving original data
                step = Step(
                    index=step_data.get("index", original_step.index if original_step else step_idx + 1),
                    title=step_data.get("title", original_step.title if original_step else f"Step {step_idx + 1}"),
                    description=step_data.get("description", original_step.description if original_step else ""),
                    teaching_guidance=step_data.get("teaching_guidance", ""),  # Instructions for implementing agent
                    dependencies=step_data.get("dependencies", original_step.dependencies if original_step else [])
                )
                steps.append(step)

            phase = Phase(
                index=phase_data.get("index", original_phase.index if original_phase else phase_idx + 1),
                name=phase_data.get("name", original_phase.name if original_phase else f"Phase {phase_idx + 1}"),
                description=phase_data.get("description", original_phase.description if original_phase else ""),
                steps=steps
            )
            enriched_phases.append(phase)

        return enriched_phases, global_notes

    except (json.JSONDecodeError, KeyError, IndexError) as e:
        print(f"Error parsing teaching enrichment result: {e}")
        print(f"Falling back to original phases without teaching annotations")

        # Return original phases with generic teaching notes
        return original_phases, f"(Teaching enrichment failed: {str(e)})"


def enrich_with_teaching(
    phases: List[Phase],
    goals: ProjectGoals,
    skill_level: str = "intermediate"
) -> tuple[List[Phase], str]:
    """
    High-level function to enrich phases with comprehensive implementation guidance for AI execution.

    This is the main entry point for implementation guidance enrichment. It:
    1. Creates the TeacherAgent (now an implementation guidance specialist)
    2. Creates the enrichment task
    3. Executes the task
    4. Merges detailed implementation guidance into the phases

    Args:
        phases: List of Phase objects from PhaseDesignerAgent
        goals: Learning and technical objectives
        skill_level: Target skill level for users of the final program

    Returns:
        Tuple of (enriched phases with comprehensive teaching_guidance fields,
                 global implementation notes for autonomous AI execution)

    Usage:
        >>> enriched_phases, global_notes = enrich_with_teaching(phases, goals, "intermediate")
        >>> print(enriched_phases[0].steps[0].teaching_guidance)
        "Create project structure with src/ directory containing models/, routes/, and utils/.
        Use Python 3.10+ with FastAPI and SQLite. Include __init__.py files and a main.py entry point..."
    """
    from crewai import Crew

    agent = create_teacher_agent()
    task = create_teaching_enrichment_task(agent, phases, goals, skill_level)

    # Execute the task through a Crew
    crew = Crew(agents=[agent], tasks=[task], verbose=True)
    output = crew.kickoff()
    result = output.raw

    # Parse and merge teaching guidance
    enriched_phases, global_notes = parse_teaching_enrichment_result(result, phases)

    return enriched_phases, global_notes
