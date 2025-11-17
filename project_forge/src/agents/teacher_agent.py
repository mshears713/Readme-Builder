"""
TeacherAgent - Adds educational feature guidance to project plans.

This agent takes the structured phase/step plan from PhaseDesignerAgent and
enriches it with instructions for building educational features. It adds
"teaching_guidance" fields to each step that tell the implementing AI agent
what educational elements to incorporate into the UI and documentation.

Key responsibilities:
- Add "teaching_guidance" instructions to each step
- Specify what educational features should be built into the program
- Guide the agent to include tooltips, examples, documentation, and tutorials
- Ensure the final program helps users learn as they use it
- Make the program itself a teaching tool

The output is an enriched ProjectPlan where every step includes instructions
for what educational features the implementing agent should build.

Teaching Note:
    This agent embodies the "meta" nature of Project Forge. We're not teaching
    the USER how to code - we're instructing the AGENT what educational features
    to build INTO the program so the program itself becomes a learning tool.

    Good teaching guidance:
    - Specifies concrete educational features to build (tooltips, examples, docs)
    - Focuses on making the program teach its users
    - Instructs the agent what to include, not what the user should learn
    - Creates a program that guides users as they interact with it
"""

from crewai import Agent, Task
from typing import List, Dict, Any
import json

from ..models.project_models import ProjectIdea, ProjectGoals, Phase, Step, ProjectPlan


def create_teacher_agent() -> Agent:
    """
    Create the TeacherAgent that instructs AI agents on educational features to build.

    This agent understands how to make software educational and guides the
    implementing AI agent to build features that help users learn. It focuses
    on specifying concrete educational elements to include in the program.

    Returns:
        CrewAI Agent configured for educational feature guidance

    Teaching Note:
        This agent writes instructions for the IMPLEMENTING AGENT, not lessons
        for the user. It tells the agent what tooltips, examples, documentation,
        and interactive features to build into the program.
    """
    return Agent(
        role="Educational Product Designer and Learning Experience Architect",
        goal="Guide AI agents to build programs with rich educational features that help users learn through interaction",
        backstory="""You are an expert at designing educational software and
        interactive learning experiences. You specialize in instructing AI agents
        on what educational features to build into programs.

        Your expertise includes:
        - Designing intuitive UI elements that guide users (tooltips, hints, examples)
        - Creating inline documentation that teaches concepts in context
        - Building interactive tutorials and guided walkthroughs
        - Incorporating progressive disclosure of complexity
        - Making programs self-documenting and discoverable
        - Designing help systems and contextual assistance

        Your design philosophy:
        - Programs should teach users how to use them
        - Learning happens through interaction and exploration
        - Good UI design includes educational scaffolding
        - Documentation should be embedded where users need it
        - Examples and demonstrations are more effective than pure text
        - The program itself is the teaching tool

        You write instructions that tell the implementing agent to:
        - Add tooltips explaining features and concepts when users hover
        - Include inline code comments that explain patterns and decisions
        - Create example/demo sections showing how things work
        - Build help sections with clear explanations and examples
        - Add interactive elements that demonstrate concepts
        - Include "Learn More" links to deeper explanations
        - Create guided tutorials or walkthroughs for first-time users
        - Display hints and tips at appropriate moments

        You DO NOT:
        - Write lessons teaching the user how to code
        - Explain programming concepts to the user directly
        - Focus on theory rather than practical UI features
        - Write generic suggestions without specific implementation details""",
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
Add educational feature guidance to this project plan.

LEARNING GOALS (what users should learn from using the program):
{chr(10).join(f'- {goal}' for goal in goals.learning_goals)}

TECHNICAL GOALS (what the program does):
{chr(10).join(f'- {goal}' for goal in goals.technical_goals)}

USER SKILL LEVEL: {skill_level}

CURRENT PLAN STRUCTURE:
{chr(10).join(phases_summary)}

Your task is to:
1. Add a "teaching_guidance" instruction to EVERY step
2. Create global teaching notes for the implementing AI agent

CRITICAL: You are NOT teaching the user how to code. You are instructing the
implementing AI agent what educational features to BUILD INTO the program.

GUIDELINES FOR "teaching_guidance" INSTRUCTIONS:
- Keep to 1-3 sentences
- Specify concrete UI/documentation features to include
- Tell the agent WHAT to build (tooltips, examples, help sections, etc.)
- Focus on making the program itself educational
- Be specific about what educational elements to add
- Consider the {skill_level} of users who will use the final program

EXAMPLES OF GOOD INSTRUCTIONS:
✓ "Add inline code comments explaining the dataclass pattern and include a tooltip in the UI showing an example of how dataclasses reduce boilerplate vs. traditional classes."
✓ "Create a help section documenting the API endpoints with example requests/responses, and include tooltips explaining RESTful conventions when users hover over endpoint paths."
✓ "Include a 'Database Design' section in the documentation showing the schema diagram, and add comments in the database functions explaining the separation of concerns pattern."
✓ "Build an interactive demo showing async/await in action - let users click to see the execution flow, and include a side-by-side comparison with synchronous code."

EXAMPLES OF BAD INSTRUCTIONS:
✗ "Learn about databases" (this teaches the user, not the agent)
✗ "You'll understand how to use SQLite here" (this is a lesson, not a build instruction)
✗ "Make sure users learn programming" (too vague, no specific features)
✗ "Add documentation" (not specific enough about what to document or how)

GUIDELINES FOR GLOBAL TEACHING NOTES:
- Write 3-5 sentences instructing the agent on overall educational strategy
- Specify what overarching educational features to include
- Describe the learning experience users should have
- Connect to the stated learning goals
- Focus on the program as a teaching tool

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
                    "teaching_guidance": "YOUR INSTRUCTION TO THE IMPLEMENTING AGENT HERE (1-3 sentences specifying what educational features to build)",
                    "dependencies": []
                }},
                ...
            ]
        }},
        ...
    ],
    "global_teaching_notes": "Your 3-5 sentence overview of the educational strategy for the implementing agent to follow..."
}}

IMPORTANT:
- Preserve all existing step data (title, description, dependencies, indices)
- Only ADD the "teaching_guidance" field and global_teaching_notes
- Write guidance for ALL {sum(len(p.steps) for p in phases)} steps
- Make each instruction specific to that step's implementation
- Ensure coherent educational features across the phases
- Remember: You're instructing an AI agent what to BUILD, not teaching a user how to CODE
"""

    return Task(
        description=description,
        expected_output="JSON object with enriched phases (including teaching_guidance for all steps) and global teaching notes for the implementing agent",
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
    High-level function to enrich phases with educational feature guidance.

    This is the main entry point for teaching enrichment. It:
    1. Creates the TeacherAgent
    2. Creates the enrichment task
    3. Executes the task
    4. Merges educational guidance into the phases

    Args:
        phases: List of Phase objects from PhaseDesignerAgent
        goals: Learning and technical objectives
        skill_level: Target user's skill level for the final program

    Returns:
        Tuple of (enriched phases with teaching_guidance fields, global teaching notes for implementing agent)

    Usage:
        >>> enriched_phases, global_notes = enrich_with_teaching(phases, goals, "intermediate")
        >>> print(enriched_phases[0].steps[0].teaching_guidance)
        "Add inline comments explaining the project structure and include a README section with package organization diagram..."
    """
    agent = create_teacher_agent()
    task = create_teaching_enrichment_task(agent, phases, goals, skill_level)

    # Execute the task
    result = task.execute()

    # Parse and merge teaching guidance
    enriched_phases, global_notes = parse_teaching_enrichment_result(result, phases)

    return enriched_phases, global_notes
