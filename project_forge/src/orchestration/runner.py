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

    Phase 1 implementation: Just print the raw idea and configuration.
    Phase 2 will add: crew initialization and execution.
    Phase 4 will add: README/PRD file writing.
    Phase 5 will add: advanced options and error handling.
    """
    args = parse_arguments()

    # Get the project idea
    idea = get_project_idea(args)

    if not idea:
        print("Error: No project idea provided.", file=sys.stderr)
        print("Usage: python -m src.orchestration.runner \"Your project idea\"", file=sys.stderr)
        sys.exit(1)

    # Phase 1: Just print the raw idea and parameters
    print("=" * 80)
    print("PROJECT FORGE - Phase 1 Placeholder")
    print("=" * 80)
    print()
    print(f"Raw Project Idea:")
    print(f"  {idea}")
    print()
    print(f"Configuration:")
    print(f"  Skill Level:  {args.skill}")
    print(f"  Complexity:   {args.complexity}")
    print(f"  Time Frame:   {args.time}")
    print(f"  Output Dir:   {args.output_dir}")
    print(f"  Verbose:      {args.verbose}")
    print()
    print("=" * 80)
    print("Phase 1 Status: Foundation complete ✓")
    print("Next: Phase 2 will implement agent logic and crew execution")
    print("=" * 80)

    # TODO Phase 2: Initialize crew
    # from .crew_config import create_crew
    # crew = create_crew()

    # TODO Phase 2: Run the crew with the idea
    # result = crew.kickoff(inputs={"idea": idea, "skill": args.skill, ...})

    # TODO Phase 4: Write the README/PRD to disk
    # output_path = Path(args.output_dir) / "PROJECT_README.md"
    # output_path.parent.mkdir(parents=True, exist_ok=True)
    # output_path.write_text(result.final_output)
    # print(f"README/PRD written to: {output_path}")


if __name__ == "__main__":
    main()
