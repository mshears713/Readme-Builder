"""
Project Forge CLI entrypoint.

This is the main entry point for the Project Forge system. It accepts a raw
project idea via command line, orchestrates the multi-agent crew, and outputs
the final README/PRD document.

Usage:
    python -m src.orchestration.runner "Build a Streamlit app for tracking habits"

Phase 1: Placeholder implementation
Phase 2: Planning crew (ConceptExpander, GoalsAnalyzer, FrameworkSelector)
Phase 3: Full plan crew (+ PhaseDesigner, TeacherAgent, EvaluatorAgent)
Phase 4: Complete pipeline (+ PRDWriterAgent, file output)
"""

import sys
import argparse
import logging
import os
from pathlib import Path
from typing import Optional
from datetime import datetime


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

    parser.add_argument(
        "--phase",
        type=int,
        choices=[2, 3, 4],
        default=4,
        help="Which phase to run: 2 (planning only), 3 (full plan), or 4 (complete with README output)"
    )

    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level for detailed execution tracking"
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


def setup_logging(log_level: str, verbose: bool) -> logging.Logger:
    """
    Configure logging for the Project Forge pipeline.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        verbose: Whether to enable verbose output

    Returns:
        Configured logger instance

    Teaching Note:
        Proper logging is essential for debugging multi-agent systems.
        We log:
        - Which agents are running
        - What decisions they make
        - Any errors or warnings
        - Performance metrics (timing, token usage, etc.)

        This makes it much easier to understand what's happening and
        troubleshoot issues.
    """
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    logger = logging.getLogger("project_forge")

    if verbose:
        logger.setLevel(logging.DEBUG)

    return logger


def main():
    """
    Main CLI entrypoint for Project Forge.

    Phase 2: Planning crew (ConceptExpander, GoalsAnalyzer, FrameworkSelector)
    Phase 3: Full plan crew (+ PhaseDesigner, TeacherAgent, EvaluatorAgent)
    Phase 4: Complete pipeline (+ PRDWriterAgent, file output, logging, error handling)
    Phase 5: Advanced options and refinements

    Teaching Note:
        This is the user-facing entry point. It:
        1. Parses command-line arguments
        2. Sets up logging
        3. Validates input
        4. Runs the appropriate pipeline phase
        5. Handles errors gracefully
        6. Writes output to disk (Phase 4+)
        7. Provides user feedback throughout

        Error handling is critical here - we want to give users clear,
        actionable error messages rather than cryptic stack traces.
    """
    args = parse_arguments()

    # Set up logging
    logger = setup_logging(args.log_level, args.verbose)
    logger.info("Project Forge starting...")

    # Get the project idea
    idea = get_project_idea(args)

    if not idea:
        logger.error("No project idea provided")
        print("Error: No project idea provided.", file=sys.stderr)
        print("Usage: python -m src.orchestration.runner \"Your project idea\"", file=sys.stderr)
        sys.exit(1)

    # Validate idea length
    if len(idea.strip()) < 10:
        logger.error(f"Project idea too short: {len(idea)} characters")
        print("Error: Project idea must be at least 10 characters long.", file=sys.stderr)
        sys.exit(1)

    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        logger.error("OPENAI_API_KEY environment variable not set")
        print("Error: OPENAI_API_KEY not found in environment.", file=sys.stderr)
        print("Please set it in your .env file or environment variables.", file=sys.stderr)
        sys.exit(1)

    print("=" * 80)
    print(f"PROJECT FORGE - Phase {args.phase}")
    print("=" * 80)
    print()
    print(f"Configuration:")
    print(f"  Skill Level:  {args.skill}")
    print(f"  Complexity:   {args.complexity}")
    print(f"  Time Frame:   {args.time}")
    print(f"  Verbose:      {args.verbose}")
    print(f"  Log Level:    {args.log_level}")
    print(f"  Phase:        {args.phase}")
    print(f"  Output Dir:   {args.output_dir}")
    print()

    logger.info(f"Running Phase {args.phase} with skill level: {args.skill}")
    logger.debug(f"Full idea text: {idea}")

    try:
        if args.phase == 2:
            # Phase 2: Run planning crew only
            logger.info("Starting Phase 2: Planning crew")
            from .crew_config import create_planning_crew

            logger.debug("Creating planning crew agents...")
            result = create_planning_crew(
                raw_idea=idea,
                skill_level=args.skill,
                verbose=args.verbose
            )
            logger.info("Phase 2 planning crew completed successfully")

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
            print("Use --phase 3 to generate full project plan with phases and teaching")
            print("=" * 80)

        elif args.phase == 3:
            # Phase 3: Run full plan crew
            logger.info("Starting Phase 3: Full plan crew with teaching")
            from .crew_config import create_full_plan_crew

            logger.debug("Creating full plan crew with all agents...")
            result = create_full_plan_crew(
                raw_idea=idea,
                skill_level=args.skill,
                verbose=args.verbose,
                max_iterations=2
            )
            logger.info(f"Phase 3 completed after {result.iterations} iteration(s)")

            # Display final summary
            plan = result.project_plan
            eval_result = result.evaluation

            print("=" * 80)
            print("FULL PLAN SUMMARY")
            print("=" * 80)
            print()
            print("PROJECT CONCEPT:")
            print(f"  {plan.idea.refined_summary}")
            print()
            print("LEARNING GOALS:")
            for i, goal in enumerate(plan.goals.learning_goals, 1):
                print(f"  {i}. {goal}")
            print()
            print("TECHNOLOGY STACK:")
            print(f"  Frontend:  {plan.framework.frontend or 'None (CLI-only)'}")
            print(f"  Backend:   {plan.framework.backend or 'None'}")
            print(f"  Storage:   {plan.framework.storage or 'None'}")
            if plan.framework.special_libs:
                print(f"  Libraries: {', '.join(plan.framework.special_libs)}")
            print()
            print("PROJECT STRUCTURE:")
            for phase in plan.phases:
                print(f"  Phase {phase.index}: {phase.name} ({len(phase.steps)} steps)")
            total_steps = sum(len(p.steps) for p in plan.phases)
            print(f"  Total: {len(plan.phases)} phases, {total_steps} steps")
            print()
            print("TEACHING ENRICHMENT:")
            steps_with_teaching = sum(
                1 for p in plan.phases for s in p.steps
                if s.what_you_learn and len(s.what_you_learn.strip()) > 10
            )
            print(f"  {steps_with_teaching}/{total_steps} steps have learning annotations")
            print(f"  Global notes: {len(plan.teaching_notes)} characters")
            print()
            print("EVALUATION:")
            print(f"  Status: {'✓ Approved' if eval_result.approved else '✗ Needs work'}")
            print(f"  Iterations: {result.iterations}")
            if eval_result.scores:
                from ..tools.rubric_tool import RubricCriterion
                for criterion, score in eval_result.scores.items():
                    print(f"  {criterion.value.title()}: {score.score}/10")
            print()
            print("=" * 80)
            print("Phase 3 Status: Full plan generation complete ✓")
            print("Use --phase 4 to generate README/PRD output to file")
            print("=" * 80)

        elif args.phase == 4:
            # Phase 4: Complete pipeline with README generation and file output
            logger.info("Starting Phase 4: Complete pipeline with README generation")
            from .crew_config import create_complete_pipeline

            logger.debug("Running complete pipeline with all agents...")
            start_time = datetime.now()

            result = create_complete_pipeline(
                raw_idea=idea,
                skill_level=args.skill,
                verbose=args.verbose,
                max_iterations=2
            )

            elapsed_time = (datetime.now() - start_time).total_seconds()
            logger.info(f"Complete pipeline finished in {elapsed_time:.2f} seconds")

            # Write README to disk
            output_dir = Path(args.output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

            output_filename = f"{result.project_name}_README.md"
            output_path = output_dir / output_filename

            logger.info(f"Writing README to: {output_path}")
            output_path.write_text(result.readme_content, encoding='utf-8')
            logger.info(f"README written successfully ({len(result.readme_content)} characters)")

            # Display final summary
            plan = result.project_plan
            eval_result = result.evaluation

            print("=" * 80)
            print("COMPLETE PIPELINE SUMMARY")
            print("=" * 80)
            print()
            print("PROJECT CONCEPT:")
            print(f"  {plan.idea.refined_summary}")
            print()
            print("LEARNING GOALS:")
            for i, goal in enumerate(plan.goals.learning_goals, 1):
                print(f"  {i}. {goal}")
            print()
            print("TECHNOLOGY STACK:")
            print(f"  Frontend:  {plan.framework.frontend or 'None (CLI-only)'}")
            print(f"  Backend:   {plan.framework.backend or 'None'}")
            print(f"  Storage:   {plan.framework.storage or 'None'}")
            if plan.framework.special_libs:
                print(f"  Libraries: {', '.join(plan.framework.special_libs)}")
            print()
            print("PROJECT STRUCTURE:")
            for phase in plan.phases:
                print(f"  Phase {phase.index}: {phase.name} ({len(phase.steps)} steps)")
            total_steps = sum(len(p.steps) for p in plan.phases)
            print(f"  Total: {len(plan.phases)} phases, {total_steps} steps")
            print()
            print("README OUTPUT:")
            print(f"  File:       {output_path}")
            print(f"  Size:       {len(result.readme_content)} characters")
            print(f"  Project:    {result.project_name}")
            print()
            print("EVALUATION:")
            print(f"  Status:     {'✓ Approved' if eval_result.approved else '✗ Needs work'}")
            print(f"  Iterations: {result.iterations}")
            if eval_result.scores:
                from ..tools.rubric_tool import RubricCriterion
                for criterion, score in eval_result.scores.items():
                    print(f"  {criterion.value.title()}: {score.score}/10")
            print()
            print("EXECUTION TIME:")
            print(f"  Total:      {elapsed_time:.2f} seconds")
            print()
            print("=" * 80)
            print("Phase 4 Status: Complete pipeline finished successfully ✓")
            print(f"README/PRD written to: {output_path}")
            print("=" * 80)
            print()
            print("Next steps:")
            print(f"  1. Review the generated README: {output_path}")
            print("  2. Feed it to Claude Code to implement the project")
            print("  3. Use Phase 5 presets for more control over output")
            print()

    except KeyboardInterrupt:
        logger.warning("Pipeline interrupted by user")
        print("\nPipeline interrupted by user.", file=sys.stderr)
        sys.exit(130)
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        print(f"Validation error: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        print(f"File error: {e}", file=sys.stderr)
        print("Please check that all required files are present.", file=sys.stderr)
        sys.exit(1)
    except PermissionError as e:
        logger.error(f"Permission error: {e}")
        print(f"Permission error: {e}", file=sys.stderr)
        print(f"Please check write permissions for: {args.output_dir}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"Error running crew: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
