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
import json

from ..models.project_models import ProjectPlan, Phase


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
        with deep experience in both software engineering and AI-assisted development.

        Your documentation is specifically designed for AI agents like Claude Code that
        will execute the entire project autonomously from start to finish. Your READMEs
        enable AI to work independently for extended periods (1+ hours) without user intervention.

        Your documentation is known for:
        - Crystal-clear, sequential instructions that AI can follow autonomously
        - Complete technical specifications with no ambiguity or missing details
        - Comprehensive context that explains "what", "why", and "how" for each step
        - Self-contained instructions requiring no external research or clarification
        - Detailed implementation guidance embedded directly in each step
        - Clear dependencies and execution order
        - Realistic scope that can be completed in one continuous session

        You excel at creating "executable specifications" - documentation so complete
        and clear that an AI agent can build the entire project end-to-end without
        stopping to ask questions or wait for user input.

        Your READMEs are comprehensive, technically precise, and structured for
        autonomous execution. AI agents love your docs because they can work
        independently and deliver complete, working projects.""",
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

Your task is to convert this structured plan into a comprehensive README designed for
AUTONOMOUS END-TO-END EXECUTION by an AI agent (like Claude Code).

CRITICAL: This README will be given to an AI agent that will execute ALL 5 phases and
ALL ~50 steps in ONE CONTINUOUS SESSION without user intervention. The AI should be able
to work for 1+ hours autonomously and deliver a complete, working project.

# PROJECT TITLE (derive from the refined concept)

## Overview
[Write a compelling 2-3 paragraph overview that:
- Explains what this project is and why it's valuable
- Highlights the key learning outcomes
- Mentions the target audience/skill level
- Sets clear expectations: This is designed for AUTONOMOUS EXECUTION by AI
- Estimates total completion time (typically 1-3 hours for full execution)]

## Autonomous Execution Guide

**For AI Agents (Claude Code, etc.):**

This README is structured for complete autonomous execution. You should:
1. Execute all 5 phases sequentially from start to finish
2. Complete all ~50 steps in order, respecting dependencies
3. Work continuously without requiring user input or approval between steps
4. Create all files, implement all features, and test thoroughly
5. Only surface the final working project to the user when complete

**Execution Strategy:**
- Follow steps in numerical order (1 → 50)
- Check dependencies before starting each step
- Create comprehensive implementations (not stubs or TODOs)
- Include proper error handling and edge cases
- Write clear code comments and documentation as you go
- Test each component as you build it
- Save all progress - the user should only review after completion

## Teaching Goals

### Learning Goals
[List all learning goals with brief explanations of what the final program will teach its users]

### Technical Goals
[List all technical goals with brief explanations of what will be built]

### Priority Notes
[Include the priority_notes from the goals]

## Technology Stack

[For each technology choice (frontend, backend, storage, special libraries):
- State the choice
- Explain WHY it was chosen
- Note key features the AI should leverage
- Mention critical setup requirements]

**Framework Rationale:**
[Explain how this stack was chosen based on skill level and project goals]

## Architecture Overview

[Create a comprehensive architecture description that the AI can follow:
- How all components fit together
- Complete data flow through the system
- Key design patterns and architectural decisions
- Directory structure and file organization
- Integration points between components
- ASCII diagram if helpful]

## Implementation Plan

**IMPORTANT**: Execute all phases sequentially. Complete each phase entirely before moving to the next.
Each step includes complete implementation guidance. Do not create stubs or placeholders -
implement fully functional code at each step.

[For EACH phase, create a detailed section:]

### Phase [N]: [Phase Name]

**Overview:** [Phase description - what this phase accomplishes and delivers]

**Completion Criteria:** [What should be working when this phase is done]

**Steps:**

[For EACH step in the phase:]

#### Step [N]: [Step Title]

**What to Build:**
[Detailed step description with complete specifications]

**Implementation Details:**
[Comprehensive technical guidance from teaching_guidance field:
- Specific code patterns to use
- File names and locations
- Function/class signatures
- Key algorithms or logic
- Error handling approaches
- Testing considerations
- Documentation to include (docstrings, comments, help text)
- Any UI elements (tooltips, help sections, examples) to build into the program]

**Dependencies:** [List prerequisite steps - complete these first]

**Acceptance Criteria:**
[How to verify this step is complete - what should work?]

---

[Repeat for all phases and steps]

## Implementation Strategy for AI Agents

[Comprehensive guidance for autonomous execution:
- Start with Phase 1, Step 1 and work sequentially
- Create proper project structure before writing code
- Implement complete, production-ready code (not TODOs or stubs)
- Test each component as you build it
- Handle errors and edge cases throughout
- Write comprehensive docstrings and comments
- Build all UI elements and documentation specified in steps
- Ensure the final program is self-documenting and user-friendly
- The final deliverable should be a fully working, polished program]

## Setup Instructions

[Complete, detailed setup instructions:
- Python version requirements (be specific: Python 3.10+, etc.)
- Virtual environment creation commands
- ALL package dependencies with versions
- Configuration files needed (with example content)
- Environment variables required (with example .env)
- Initial project directory structure to create
- Any database initialization or migrations
- Any external service setup (APIs, etc.)]

## Testing Strategy

[Guidance for testing throughout development:
- Unit tests to write (if appropriate for skill level)
- Integration testing approach
- Manual testing checklist
- Edge cases to verify
- How to validate each phase is working]

## Success Metrics

[Define what "complete" means:
- All functional requirements implemented
- All phases and steps completed
- Program runs without errors
- Key features work as specified
- Code is well-documented
- User-facing documentation exists]

## Project Completion Checklist

- [ ] All 50 steps completed
- [ ] All phases deliver working functionality
- [ ] No TODO comments or placeholder code
- [ ] Error handling implemented
- [ ] Code is documented (docstrings + comments)
- [ ] README or user guide included (if applicable)
- [ ] Program tested and working
- [ ] Repository is clean and organized

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
        expected_output="""A complete, well-formatted README markdown document (5000+ characters)
        designed for AUTONOMOUS END-TO-END EXECUTION by AI agents. Must include all sections:
        Overview, Autonomous Execution Guide, Teaching Goals, Technology Stack, Architecture,
        detailed Implementation Plan with all 5 phases and ~50 steps (including comprehensive
        Implementation Details for each step), Implementation Strategy, Setup Instructions,
        Testing Strategy, Success Metrics, and Project Completion Checklist. The document
        must be so complete and clear that an AI agent can execute all steps sequentially
        for 1+ hours without user intervention and deliver a fully working project.""",
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
