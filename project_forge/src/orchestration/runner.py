"""
Project Forge CLI entrypoint.

This is the main entry point for the Project Forge system. It accepts a raw
project idea via command line, orchestrates the multi-agent crew, and outputs
the final README/PRD document.

Usage:
    python -m src.orchestration.runner "Build a Streamlit app for tracking habits"

Phase 1: This is a placeholder implementation that just prints the raw idea.
Real crew execution will be implemented in Phase 2.
"""

import sys
import argparse
from pathlib import Path
from typing import Optional


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="Project Forge - Generate comprehensive project plans and READMEs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python -m src.orchestration.runner "Build a wildfire grant dashboard"
    python -m src.orchestration.runner "Create an AI agent system for code review"
    python -m src.orchestration.runner --skill beginner "Make a todo app"
        """
    )

    parser.add_argument(
        "idea",
        type=str,
        nargs="?",
        help="The raw project idea (can also be piped via stdin)"
    )

    parser.add_argument(
        "--skill",
        type=str,
        choices=["beginner", "intermediate", "advanced"],
        default="intermediate",
        help="Your skill level (affects framework choices and teaching detail)"
    )

    parser.add_argument(
        "--complexity",
        type=str,
        choices=["low", "medium", "high"],
        default="medium",
        help="Desired project complexity"
    )

    parser.add_argument(
        "--time",
        type=str,
        default="1-2 weeks",
        help="Time constraint for the project (e.g., '1 week', '1-2 weeks')"
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="output",
        help="Directory to save the generated README/PRD"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging of agent actions"
    )

    return parser.parse_args()


def get_project_idea(args: argparse.Namespace) -> Optional[str]:
    """
    Get the project idea from arguments or stdin.

    Args:
        args: Parsed command-line arguments

    Returns:
        The raw project idea string, or None if not provided
    """
    if args.idea:
        return args.idea

    # Check if stdin has data (piped input)
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()

    return None


def main():
    """
    Main CLI entrypoint for Project Forge.

    Phase 2 implementation: Run the planning crew and display results.
    - ConceptExpanderAgent: refine the raw idea
    - GoalsAnalyzerAgent: extract learning and technical goals
    - FrameworkSelectorAgent: choose appropriate tech stack
    - RubricTool: evaluate concept clarity

    Phase 3 will add: PhaseDesigner, TeacherAgent, EvaluatorAgent.
    Phase 4 will add: PRDWriterAgent and file output.
    Phase 5 will add: advanced options and error handling.
    """
    args = parse_arguments()

    # Get the project idea
    idea = get_project_idea(args)

    if not idea:
        print("Error: No project idea provided.", file=sys.stderr)
        print("Usage: python -m src.orchestration.runner \"Your project idea\"", file=sys.stderr)
        sys.exit(1)

    print("=" * 80)
    print("PROJECT FORGE - Phase 2")
    print("=" * 80)
    print()
    print(f"Configuration:")
    print(f"  Skill Level:  {args.skill}")
    print(f"  Complexity:   {args.complexity}")
    print(f"  Time Frame:   {args.time}")
    print(f"  Verbose:      {args.verbose}")
    print()

    # Phase 2: Run the planning crew
    # This executes ConceptExpander → GoalsAnalyzer → FrameworkSelector
    try:
        from .crew_config import create_planning_crew

        # Run the planning crew with the raw idea
        result = create_planning_crew(
            raw_idea=idea,
            skill_level=args.skill,
            verbose=args.verbose
        )

        # Display final summary
        print("=" * 80)
        print("PLANNING SUMMARY")
        print("=" * 80)
        print()
        print("PROJECT CONCEPT:")
        print(f"  {result.project_idea.refined_summary}")
        print()
        print("LEARNING GOALS:")
        for i, goal in enumerate(result.project_goals.learning_goals, 1):
            print(f"  {i}. {goal}")
        print()
        print("TECHNICAL GOALS:")
        for i, goal in enumerate(result.project_goals.technical_goals, 1):
            print(f"  {i}. {goal}")
        print()
        print("TECHNOLOGY STACK:")
        print(f"  Frontend:  {result.framework_choice.frontend or 'None (CLI-only)'}")
        print(f"  Backend:   {result.framework_choice.backend or 'None'}")
        print(f"  Storage:   {result.framework_choice.storage or 'None'}")
        if result.framework_choice.special_libs:
            print(f"  Libraries: {', '.join(result.framework_choice.special_libs)}")
        print()
        print("QUALITY METRICS:")
        print(f"  Concept Clarity: {result.clarity_score.score}/10")
        print(f"  Feedback: {result.clarity_score.feedback}")
        print()
        print("=" * 80)
        print("Phase 2 Status: Planning crew complete ✓")
        print("Next: Phase 3 will add phase design and teaching enrichment")
        print("=" * 80)

    except Exception as e:
        print(f"Error running planning crew: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # TODO Phase 4: Write the README/PRD to disk
    # output_path = Path(args.output_dir) / "PROJECT_README.md"
    # output_path.parent.mkdir(parents=True, exist_ok=True)
    # output_path.write_text(result.final_output)
    # print(f"README/PRD written to: {output_path}")


if __name__ == "__main__":
    main()
