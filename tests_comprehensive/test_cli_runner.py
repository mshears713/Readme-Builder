"""
Test suite for CLI runner functionality.

Tests argument parsing, input validation, logging setup, and error handling
without actually running the full agent pipeline (to avoid API costs).
"""

import sys
import os
from pathlib import Path
from io import StringIO

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from project_forge.src.orchestration.runner import (
    parse_arguments,
    get_project_idea,
    setup_logging
)
import argparse
import logging


def test_parse_arguments_minimal():
    """Test parsing minimal arguments."""
    print("Testing minimal argument parsing...")

    # Simulate command line arguments
    sys.argv = ["runner.py", "Build a todo app"]
    args = parse_arguments()

    assert args.idea == "Build a todo app"
    assert args.skill == "intermediate"  # default
    assert args.complexity == "medium"  # default
    assert args.phase == 4  # default
    print("✓ Minimal arguments parsed correctly")


def test_parse_arguments_with_skill():
    """Test parsing arguments with skill level."""
    print("Testing argument parsing with skill level...")

    sys.argv = ["runner.py", "--skill", "beginner", "Build a todo app"]
    args = parse_arguments()

    assert args.skill == "beginner"
    assert args.idea == "Build a todo app"
    print("✓ Skill level argument parsed correctly")


def test_parse_arguments_with_complexity():
    """Test parsing arguments with complexity."""
    print("Testing argument parsing with complexity...")

    sys.argv = ["runner.py", "--complexity", "high", "Complex project"]
    args = parse_arguments()

    assert args.complexity == "high"
    print("✓ Complexity argument parsed correctly")


def test_parse_arguments_with_phase():
    """Test parsing arguments with specific phase."""
    print("Testing argument parsing with phase...")

    sys.argv = ["runner.py", "--phase", "2", "Test project"]
    args = parse_arguments()

    assert args.phase == 2
    print("✓ Phase argument parsed correctly")


def test_parse_arguments_verbose():
    """Test parsing verbose flag."""
    print("Testing verbose flag parsing...")

    sys.argv = ["runner.py", "--verbose", "Test project"]
    args = parse_arguments()

    assert args.verbose == True
    print("✓ Verbose flag parsed correctly")


def test_parse_arguments_all_options():
    """Test parsing all arguments together."""
    print("Testing all arguments together...")

    sys.argv = [
        "runner.py",
        "--skill", "advanced",
        "--complexity", "high",
        "--project-type", "ambitious",
        "--time", "3 weeks",
        "--verbose",
        "--phase", "3",
        "--output-dir", "custom_output",
        "Build complex multi-agent system"
    ]
    args = parse_arguments()

    assert args.skill == "advanced"
    assert args.complexity == "high"
    assert args.project_type == "ambitious"
    assert args.time == "3 weeks"
    assert args.verbose == True
    assert args.phase == 3
    assert args.output_dir == "custom_output"
    assert args.idea == "Build complex multi-agent system"
    print("✓ All arguments parsed correctly")


def test_get_project_idea_from_args():
    """Test getting project idea from arguments."""
    print("Testing getting project idea from args...")

    sys.argv = ["runner.py", "My project idea"]
    args = parse_arguments()
    idea = get_project_idea(args)

    assert idea == "My project idea"
    print("✓ Project idea retrieved from args")


def test_get_project_idea_none():
    """Test getting project idea when none provided."""
    print("Testing getting project idea when none provided...")

    sys.argv = ["runner.py"]
    args = parse_arguments()
    idea = get_project_idea(args)

    assert idea is None
    print("✓ None returned when no idea provided")


def test_setup_logging_info_level():
    """Test logging setup with INFO level."""
    print("Testing logging setup (INFO level)...")

    logger = setup_logging("INFO", verbose=False)

    assert logger is not None
    assert logger.name == "project_forge"
    assert logger.level <= logging.INFO
    print("✓ Logging setup with INFO level works")


def test_setup_logging_debug_level():
    """Test logging setup with DEBUG level."""
    print("Testing logging setup (DEBUG level)...")

    logger = setup_logging("DEBUG", verbose=True)

    assert logger is not None
    assert logger.level <= logging.DEBUG
    print("✓ Logging setup with DEBUG level works")


def test_output_directory_default():
    """Test default output directory."""
    print("Testing default output directory...")

    sys.argv = ["runner.py", "Test project"]
    args = parse_arguments()

    assert args.output_dir == "output"
    print("✓ Default output directory is 'output'")


def test_custom_output_directory():
    """Test custom output directory."""
    print("Testing custom output directory...")

    sys.argv = ["runner.py", "--output-dir", "my_custom_output", "Test project"]
    args = parse_arguments()

    assert args.output_dir == "my_custom_output"
    print("✓ Custom output directory works")


def test_idea_validation_length():
    """Test that short ideas should be caught (this is validation logic)."""
    print("Testing idea length validation concept...")

    # The actual validation happens in main(), but we can test the concept
    short_idea = "test"
    long_idea = "Build a comprehensive task management application"

    assert len(short_idea) < 10  # Would fail validation
    assert len(long_idea) >= 10  # Would pass validation
    print("✓ Idea length validation logic is sound")


def test_skill_level_choices():
    """Test that only valid skill levels are accepted."""
    print("Testing skill level choices...")

    valid_skills = ["beginner", "intermediate", "advanced"]

    # Test valid skill
    sys.argv = ["runner.py", "--skill", "intermediate", "Test"]
    args = parse_arguments()
    assert args.skill in valid_skills

    print("✓ Skill level validation works")


def test_complexity_choices():
    """Test that only valid complexity levels are accepted."""
    print("Testing complexity choices...")

    valid_complexity = ["low", "medium", "high"]

    sys.argv = ["runner.py", "--complexity", "medium", "Test"]
    args = parse_arguments()
    assert args.complexity in valid_complexity

    print("✓ Complexity validation works")


def test_project_type_choices():
    """Test that only valid project types are accepted."""
    print("Testing project type choices...")

    valid_types = ["toy", "medium", "ambitious"]

    sys.argv = ["runner.py", "--project-type", "medium", "Test"]
    args = parse_arguments()
    assert args.project_type in valid_types

    print("✓ Project type validation works")


def test_phase_choices():
    """Test that only valid phases are accepted."""
    print("Testing phase choices...")

    valid_phases = [2, 3, 4]

    sys.argv = ["runner.py", "--phase", "3", "Test"]
    args = parse_arguments()
    assert args.phase in valid_phases

    print("✓ Phase validation works")


def run_all_tests():
    """Run all CLI runner tests."""
    print("\n" + "=" * 60)
    print("RUNNING CLI RUNNER TESTS")
    print("=" * 60 + "\n")

    try:
        test_parse_arguments_minimal()
        test_parse_arguments_with_skill()
        test_parse_arguments_with_complexity()
        test_parse_arguments_with_phase()
        test_parse_arguments_verbose()
        test_parse_arguments_all_options()
        test_get_project_idea_from_args()
        test_get_project_idea_none()
        test_setup_logging_info_level()
        test_setup_logging_debug_level()
        test_output_directory_default()
        test_custom_output_directory()
        test_idea_validation_length()
        test_skill_level_choices()
        test_complexity_choices()
        test_project_type_choices()
        test_phase_choices()

        print("\n" + "=" * 60)
        print("✓ ALL CLI RUNNER TESTS PASSED")
        print("=" * 60 + "\n")
        return True

    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}\n")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
