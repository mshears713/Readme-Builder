"""
TeacherAgent - Adds pedagogical annotations to project plans.

This agent takes the structured phase/step plan from PhaseDesignerAgent and
enriches it with teaching commentary. It adds "what you'll learn" fields to
each step and creates a global teaching narrative that explains the overall
learning arc of the project.

Key responsibilities:
- Add "what_you_learn" annotations to each step
- Explain the concepts, patterns, and skills each step teaches
- Create a cohesive learning narrative across all phases
- Ensure progressive skill building from phase to phase
- Make the pedagogical value explicit and clear

The output is an enriched ProjectPlan where every step includes learning
objectives and the overall plan has teaching notes about the learning journey.

Teaching Note:
    This agent embodies the "meta" nature of Project Forge. We're not just
    generating build plans - we're creating teaching documents that help
    developers learn while they build.

    Good teaching annotations:
    - Explain WHY, not just WHAT
    - Connect to broader concepts and patterns
    - Point out learning moments and teaching opportunities
    - Progressive complexity that builds confidence
"""

from crewai import Agent, Task
from typing import List, Dict, Any
import json

from ..models.project_models import ProjectIdea, ProjectGoals, Phase, Step, ProjectPlan


def create_teacher_agent() -> Agent:
    """
    Create the TeacherAgent with specialized focus on pedagogy and learning design.

    This agent understands learning theory, progressive skill building, and how
    to make technical concepts accessible. It knows how to write teaching
    annotations that are concise but insightful.

    Returns:
        CrewAI Agent configured for teaching enrichment

    Teaching Note:
        The backstory emphasizes pedagogical expertise and the ability to
        explain complex concepts clearly. We want this agent to write
        annotations that feel like having a knowledgeable mentor explaining
        things as you work.
    """
    return Agent(
        role="Technical Educator and Learning Designer",
        goal="Enrich project plans with clear, insightful teaching annotations that make learning explicit",
        backstory="""You are an expert technical educator with deep knowledge of
        software development pedagogy and learning design.

        Your expertise includes:
        - Learning theory and progressive skill building
        - Making complex technical concepts accessible
        - Writing clear, concise explanations that stick
        - Identifying the "teachable moments" in each step
        - Creating coherent learning arcs across projects
        - Explaining not just WHAT to build but WHY and HOW it works

        Your teaching philosophy:
        - Every step is a learning opportunity
        - Concepts should build on each other naturally
        - Explain the "why" behind technical decisions
        - Connect individual steps to broader patterns and principles
        - Make learning visible and explicit
        - Appropriate challenge leads to growth

        You write annotations that:
        - Are 1-3 sentences (concise but insightful)
        - Focus on concepts, patterns, and transferable skills
        - Avoid jargon without explanation
        - Point out connections between steps
        - Celebrate learning milestones
        - Match the learner's skill level

        You DO NOT:
        - Write generic platitudes ("you'll learn a lot!")
        - Focus only on syntax or tool usage
        - Overwhelm with too much detail
        - Skip the "why" behind technical choices
        - Assume knowledge without building it progressively""",
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
    Create the task for adding teaching annotations to phases and steps.

    This task provides the existing phase structure and asks the agent to
    enrich each step with learning annotations and create global teaching notes.

    Args:
        agent: The TeacherAgent
        phases: List of Phase objects from PhaseDesignerAgent (steps have empty what_you_learn)
        goals: Learning and technical objectives for context
        skill_level: User's skill level

    Returns:
        CrewAI Task configured for teaching enrichment

    Teaching Note:
        We pass the full phase structure to the agent and ask it to return
        the same structure with added teaching annotations. This preserves
        the step details while adding pedagogical value.
    """
    # Build a summary of the phases for context
    phases_summary = []
    for phase in phases:
        steps_summary = [f"  {s.index}. {s.title}" for s in phase.steps]
        phases_summary.append(
            f"Phase {phase.index}: {phase.name}\n" + "\n".join(steps_summary)
        )

    description = f"""
Add teaching annotations to this project plan.

LEARNING GOALS:
{chr(10).join(f'- {goal}' for goal in goals.learning_goals)}

TECHNICAL GOALS:
{chr(10).join(f'- {goal}' for goal in goals.technical_goals)}

USER SKILL LEVEL: {skill_level}

CURRENT PLAN STRUCTURE:
{chr(10).join(phases_summary)}

Your task is to:
1. Add a "what_you_learn" annotation to EVERY step
2. Create global teaching notes that explain the overall learning arc

GUIDELINES FOR "what_you_learn" ANNOTATIONS:
- Keep to 1-3 sentences
- Focus on concepts, patterns, and transferable skills (not just "how to write X code")
- Explain WHY this step matters for learning
- Connect to broader software development principles
- Match the {skill_level} skill level
- Be specific and insightful, not generic

EXAMPLES OF GOOD ANNOTATIONS:
✓ "Learn how dataclasses reduce boilerplate while maintaining type safety. This pattern makes your code more maintainable and catches errors early."
✓ "Understand the relationship between HTTP endpoints and API design. RESTful conventions make your API predictable and easy to use."
✓ "Practice separating concerns by keeping database logic in dedicated functions. This makes testing easier and code more reusable."
✓ "Experience async/await patterns for I/O-bound operations. This is crucial for building responsive applications that handle multiple requests efficiently."

EXAMPLES OF BAD ANNOTATIONS:
✗ "Learn about databases" (too vague)
✗ "You'll understand how to use SQLite here" (focuses on tool, not concept)
✗ "This teaches you programming" (generic, not specific)
✗ "Master the entire stack in this step" (unrealistic scope)

GUIDELINES FOR GLOBAL TEACHING NOTES:
- Write 3-5 sentences about the overall learning journey
- Explain how the phases build on each other
- Highlight key learning milestones
- Connect to the stated learning goals
- Encourage and motivate

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
                    "what_you_learn": "YOUR TEACHING ANNOTATION HERE (1-3 sentences)",
                    "dependencies": []
                }},
                ...
            ]
        }},
        ...
    ],
    "global_teaching_notes": "Your 3-5 sentence overview of the learning arc for this entire project..."
}}

IMPORTANT:
- Preserve all existing step data (title, description, dependencies, indices)
- Only ADD the "what_you_learn" field and global_teaching_notes
- Write annotations for ALL {sum(len(p.steps) for p in phases)} steps
- Make each annotation specific to that step's content
- Ensure progressive learning across the phases
"""

    return Task(
        description=description,
        expected_output="JSON object with enriched phases (including what_you_learn for all steps) and global teaching notes",
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
                    what_you_learn=step_data.get("what_you_learn", ""),  # This is what TeacherAgent added
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
    High-level function to enrich phases with teaching annotations.

    This is the main entry point for teaching enrichment. It:
    1. Creates the TeacherAgent
    2. Creates the enrichment task
    3. Executes the task
    4. Merges teaching annotations into the phases

    Args:
        phases: List of Phase objects from PhaseDesignerAgent
        goals: Learning and technical objectives
        skill_level: User's skill level

    Returns:
        Tuple of (enriched phases with what_you_learn fields, global teaching notes)

    Usage:
        >>> enriched_phases, global_notes = enrich_with_teaching(phases, goals, "intermediate")
        >>> print(enriched_phases[0].steps[0].what_you_learn)
        "Learn how to structure a Python project with proper package organization..."
    """
    agent = create_teacher_agent()
    task = create_teaching_enrichment_task(agent, phases, goals, skill_level)

    # Execute the task
    result = task.execute()

    # Parse and merge teaching annotations
    enriched_phases, global_notes = parse_teaching_enrichment_result(result, phases)

    return enriched_phases, global_notes
