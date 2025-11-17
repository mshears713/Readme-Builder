"""
PRDWriterAgent - Converts structured ProjectPlan into comprehensive README/PRD documents.

This is the final agent in the Project Forge pipeline. It takes the complete ProjectPlan
(with idea, goals, framework choices, phases, steps, and teaching notes) and generates
a single, narrative README/PRD markdown document that can be fed to Claude Code or
another code LLM for implementation.

Key responsibilities:
- Convert structured data into clear narrative documentation
- Embed teaching notes and learning objectives throughout
- Create a standardized README structure that's easy to follow
- Include all technical details needed for implementation
- Make the document actionable and immediately usable

The output README/PRD serves as the complete specification and guide for building
the project, combining technical requirements with pedagogical commentary.

How to Modify Templates:
    The README structure is defined in the _build_readme_template() function.
    To customize the output format:

    1. Modify section headers in _build_readme_template()
    2. Adjust the markdown formatting in _format_*() helper methods
    3. Change the level of detail in phase/step descriptions
    4. Add or remove sections as needed for your use case

    The current template follows this structure:
    - Project Overview
    - Teaching Goals (Learning + Technical)
    - Technology Stack
    - Architecture Overview
    - Implementation Phases (with detailed steps)
    - Teaching Notes
    - Setup Instructions

    This structure balances technical completeness with pedagogical value,
    making it suitable for learners and experienced developers alike.
"""

from crewai import Agent, Task
from typing import List
import json

from ..models.project_models import ProjectPlan, Phase, Step


def create_prd_writer_agent() -> Agent:
    """
    Create the PRDWriterAgent with specialized prompting for README/PRD generation.

    This agent is an expert technical writer who converts structured plans into
    comprehensive, readable documentation. It maintains consistency, clarity, and
    actionability while embedding teaching commentary throughout.

    Returns:
        CrewAI Agent configured for PRD/README writing

    Teaching Note:
        This agent is the "translator" that converts our structured data models
        into natural language documentation. It needs to balance:
        - Technical accuracy (all details from the plan)
        - Narrative flow (reads like a document, not a data dump)
        - Teaching value (explains WHY, not just WHAT)
        - Actionability (Claude Code can execute it directly)

        The backstory emphasizes these qualities to guide the LLM's output style.
    """
    return Agent(
        role="Technical Documentation Specialist & PRD Writer",
        goal="Convert structured project plans into comprehensive, actionable README/PRD documents",
        backstory="""You are a world-class technical writer and documentation expert
        with deep experience in both software engineering and technical education.

        Your documentation is known for:
        - Crystal-clear structure that guides readers step-by-step
        - Perfect balance of technical detail and readability
        - Rich context that explains not just "what" but "why"
        - Actionable instructions that developers can execute immediately
        - Teaching commentary that helps learners understand concepts
        - Consistent formatting that's easy to scan and navigate

        You excel at taking structured data (plans, specs, metadata) and weaving
        it into compelling narrative documentation. You know that great documentation
        is both a reference manual AND a teaching tool.

        Your READMEs are comprehensive without being overwhelming, detailed without
        being boring, and technical without being inaccessible. Developers love
        reading your docs because they make complex projects feel approachable.""",
        allow_delegation=False,
        verbose=True
    )


def create_prd_writing_task(agent: Agent, project_plan: ProjectPlan) -> Task:
    """
    Create the task for converting a ProjectPlan into a README/PRD document.

    This task provides the agent with the complete structured plan and asks it
    to generate a comprehensive markdown document following a standard template.

    Args:
        agent: The PRDWriterAgent
        project_plan: Complete ProjectPlan with all metadata

    Returns:
        CrewAI Task configured for README/PRD writing

    Teaching Note:
        This task is where we encode the README template structure. The prompt
        includes detailed formatting instructions to ensure consistency across
        different project types. We're essentially giving the LLM a "fill in
        the blanks" template with the plan data.

        The key is to be very specific about:
        - Section ordering and headers
        - Markdown formatting conventions
        - Where to place teaching notes
        - How to format phases and steps
        - Level of detail for each section
    """
    # Extract data from the plan for the prompt
    total_steps = sum(len(phase.steps) for phase in project_plan.phases)

    # Build a structured representation of phases and steps for the prompt
    phases_summary = []
    for phase in project_plan.phases:
        phase_info = f"Phase {phase.index}: {phase.name} ({len(phase.steps)} steps)\n"
        phase_info += f"Description: {phase.description}\n"
        phase_info += "Steps:\n"
        for step in phase.steps:
            phase_info += f"  {step.index}. {step.title}\n"
            phase_info += f"      Description: {step.description}\n"
            if step.teaching_guidance:
                phase_info += f"      Teaching Guidance: {step.teaching_guidance}\n"
            if step.dependencies:
                phase_info += f"      Dependencies: Steps {', '.join(map(str, step.dependencies))}\n"
        phases_summary.append(phase_info)

    phases_text = "\n\n".join(phases_summary)

    description = f"""
Create a comprehensive README/PRD document for this project plan.

PROJECT OVERVIEW:
- Original Idea: {project_plan.idea.raw_description}
- Refined Concept: {project_plan.idea.refined_summary}
- Constraints: {json.dumps(project_plan.idea.constraints, indent=2)}

LEARNING GOALS:
{chr(10).join(f'- {goal}' for goal in project_plan.goals.learning_goals)}

TECHNICAL GOALS:
{chr(10).join(f'- {goal}' for goal in project_plan.goals.technical_goals)}

TECHNOLOGY STACK:
- Frontend: {project_plan.framework.frontend or 'None (CLI-only)'}
- Backend: {project_plan.framework.backend or 'None'}
- Storage: {project_plan.framework.storage or 'None'}
- Special Libraries: {', '.join(project_plan.framework.special_libs) if project_plan.framework.special_libs else 'None'}

PROJECT STRUCTURE:
- Total Phases: {len(project_plan.phases)}
- Total Steps: {total_steps}

DETAILED PHASES AND STEPS:
{phases_text}

GLOBAL TEACHING NOTES:
{project_plan.teaching_notes}

────────────────────────────────────────────────────────────

Your task is to convert this structured plan into a comprehensive, narrative README/PRD
document using the following structure:

# PROJECT TITLE (derive from the refined concept)

## Overview
[Write a compelling 2-3 paragraph overview that:
- Explains what this project is and why it's valuable
- Highlights the key learning outcomes
- Mentions the target audience/skill level
- Sets expectations for scope and timeline]

## Teaching Goals

### Learning Goals
[List all learning goals with brief explanations of why each matters]

### Technical Goals
[List all technical goals with brief explanations of what will be built]

### Priority Notes
[Include the priority_notes from the goals]

## Technology Stack

[For each technology choice (frontend, backend, storage, special libraries):
- State the choice
- Explain WHY it was chosen
- Note any alternatives that were considered
- Mention learning resources if applicable]

**Framework Rationale:**
[Explain how this stack was chosen based on skill level and project goals]

## Architecture Overview

[Create a high-level architecture description:
- How the components fit together
- Data flow through the system
- Key design patterns or architectural decisions
- ASCII diagram if helpful]

## Implementation Plan

[For EACH phase, create a detailed section:]

### Phase [N]: [Phase Name]

**Overview:** [Phase description - what this phase accomplishes]

**Steps:**

[For EACH step in the phase:]

#### Step [N]: [Step Title]

**Description:**
[Detailed step description]

**Educational Features to Include:**
[Teaching guidance - instructions for what educational elements to build into this step
Examples: tooltips, inline documentation, interactive demos, help sections, example code]

**Dependencies:** [List prerequisite steps if any]

**Implementation Notes:**
[Any additional context or tips]

---

[Repeat for all phases and steps]

## Global Teaching Notes

[Include the global teaching_notes with formatting and structure]

## Setup Instructions

[Create basic setup instructions based on the tech stack:
- Python version requirements
- Virtual environment setup
- Package installation
- Configuration files needed
- Environment variables
- Initial project structure]

## Development Workflow

[Suggest a recommended workflow:
- How to approach each phase
- Testing strategy
- Debugging tips
- Iteration and refinement approach]

## Success Metrics

[Define what "done" looks like:
- Functional requirements met
- Learning objectives achieved
- Quality criteria
- Testing completeness]

## Next Steps After Completion

[Suggest what to do after finishing:
- Extensions or enhancements
- Related projects to try
- Skills to practice next
- Portfolio presentation tips]

────────────────────────────────────────────────────────────

FORMATTING REQUIREMENTS:
- Use clear markdown headers (##, ###, ####)
- Use bullet points and numbered lists appropriately
- Include horizontal rules (---) between major sections
- Use **bold** for emphasis on key terms
- Use `code formatting` for technical terms, file names, commands
- Keep paragraphs concise (2-4 sentences)
- Include plenty of whitespace for readability

TONE REQUIREMENTS:
- Professional but approachable
- Educational and encouraging
- Specific and actionable
- Balanced (not too dry, not too casual)

OUTPUT:
Generate the complete README/PRD document as markdown text. This will be written
directly to a .md file, so output ONLY the markdown content with no meta-commentary
or explanations outside the document itself.
"""

    return Task(
        description=description,
        expected_output="""A complete, well-formatted README/PRD markdown document
        (5000+ characters) that includes all sections: Overview, Teaching Goals,
        Technology Stack, Architecture, detailed Implementation Plan with all phases
        and steps, Global Teaching Notes, Setup Instructions, Development Workflow,
        Success Metrics, and Next Steps. The document should be immediately usable
        by Claude Code or another LLM to implement the project.""",
        agent=agent
    )


def parse_prd_writing_result(result: str, project_plan: ProjectPlan) -> str:
    """
    Parse the PRDWriterAgent's output and return the final README text.

    In most cases, this is a simple passthrough since the agent outputs
    markdown directly. However, this function provides a hook for:
    - Cleanup or post-processing of the markdown
    - Validation that all required sections are present
    - Adding metadata headers or footers
    - Formatting standardization

    Args:
        result: Raw output from the PRDWriterAgent task
        project_plan: Original ProjectPlan (for validation/fallback)

    Returns:
        Final README/PRD markdown text ready to write to disk

    Teaching Note:
        Unlike other agents that output JSON we parse into objects, this agent
        outputs the final markdown directly. This function exists mainly for
        consistency with the other agents' parse functions, and to provide a
        place for any post-processing we might want to add later.

        You could enhance this to:
        - Validate that required sections exist
        - Add a table of contents
        - Insert metadata headers (date, version, etc.)
        - Fix common formatting issues
    """
    # For Phase 4, we just return the result as-is
    # Future enhancements could add validation or post-processing here

    # Basic validation: check that we got a substantial output
    if not result or len(result.strip()) < 500:
        raise ValueError(
            f"PRDWriter output too short ({len(result)} chars). "
            "Expected comprehensive README with 5000+ characters."
        )

    # Could add section validation here:
    # required_sections = ["Overview", "Teaching Goals", "Technology Stack", "Implementation Plan"]
    # for section in required_sections:
    #     if section not in result:
    #         logger.warning(f"Missing section: {section}")

    return result.strip()


def generate_project_name(project_plan: ProjectPlan) -> str:
    """
    Generate a filesystem-safe project name from the ProjectPlan.

    This creates a clean filename for the output README by extracting key
    words from the project summary and converting to uppercase snake_case.

    Args:
        project_plan: The complete project plan

    Returns:
        Filesystem-safe project name (e.g., "WILDFIRE_GRANT_DASHBOARD")

    Teaching Note:
        This is a utility function for generating output filenames. We want:
        - Uppercase for visibility in directory listings
        - Snake_case for filesystem compatibility
        - Key words from the project for identifiability
        - No special characters or spaces

        Example: "Build a wildfire grant tracking dashboard" → "WILDFIRE_GRANT_DASHBOARD"
    """
    # Start with the refined summary
    summary = project_plan.idea.refined_summary

    # Extract key words (simple approach: first 3-5 meaningful words)
    # Remove common filler words
    filler_words = {'a', 'an', 'the', 'for', 'to', 'of', 'in', 'on', 'with', 'and', 'or', 'but'}
    words = summary.split()
    key_words = [
        w.strip('.,!?;:').upper()
        for w in words[:10]  # Look at first 10 words
        if w.lower() not in filler_words and len(w) > 2
    ][:5]  # Take max 5 key words

    # Join with underscores
    name = '_'.join(key_words) if key_words else "PROJECT"

    # Clean up any remaining special characters
    name = ''.join(c if c.isalnum() or c == '_' else '_' for c in name)

    # Remove duplicate underscores
    while '__' in name:
        name = name.replace('__', '_')

    return name.strip('_')


# Helper functions for building README sections
# These are available for future customization

def _format_phase_section(phase: Phase) -> str:
    """
    Format a single phase into markdown (helper for template customization).

    Args:
        phase: Phase object to format

    Returns:
        Markdown text for this phase
    """
    lines = [
        f"### Phase {phase.index}: {phase.name}",
        "",
        f"**Overview:** {phase.description}",
        "",
        "**Steps:**",
        ""
    ]

    for step in phase.steps:
        lines.append(f"#### Step {step.index}: {step.title}")
        lines.append("")
        lines.append(f"**Description:** {step.description}")
        lines.append("")
        if step.teaching_guidance:
            lines.append(f"**Educational Features to Include:** {step.teaching_guidance}")
            lines.append("")
        if step.dependencies:
            dep_str = ', '.join(f"Step {d}" for d in step.dependencies)
            lines.append(f"**Dependencies:** {dep_str}")
            lines.append("")
        lines.append("---")
        lines.append("")

    return '\n'.join(lines)
