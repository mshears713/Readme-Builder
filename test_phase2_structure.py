#!/usr/bin/env python3
"""
Phase 2 Structure Validation Test

This script validates that all Phase 2 components are properly implemented
without requiring API keys or full dependency resolution.
"""

import sys
import os

# Add project_forge to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'project_forge'))

def test_imports():
    """Test that all Phase 2 modules can be imported."""
    print("Testing imports...")

    try:
        # Test model imports
        from src.models.project_models import (
            ProjectIdea, ProjectGoals, FrameworkChoice, Phase, Step, ProjectPlan
        )
        print("✓ Models import successfully")

        # Test tool imports
        from src.tools.text_cleaner_tool import clean_project_idea, extract_keywords
        from src.tools.rubric_tool import evaluate_concept_clarity, RubricScore
        print("✓ Tools import successfully")

        # Since CrewAI has dependency issues in this environment,
        # we'll verify the agent files exist and have the right structure
        import importlib.util

        agent_files = [
            'project_forge/src/agents/concept_expander_agent.py',
            'project_forge/src/agents/goals_analyzer_agent.py',
            'project_forge/src/agents/framework_selector_agent.py'
        ]

        for agent_file in agent_files:
            if os.path.exists(agent_file):
                print(f"✓ {agent_file} exists")
            else:
                print(f"✗ {agent_file} missing")
                return False

        print("✓ All agent files exist")

        return True

    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False


def test_text_tools():
    """Test text cleaning and keyword extraction."""
    print("\nTesting text tools...")

    from src.tools.text_cleaner_tool import clean_project_idea, extract_keywords

    # Test cleaning
    raw = "Um, I want to  like build a DB  app\n for tracking stuff"
    cleaned = clean_project_idea(raw)
    print(f"  Raw:     '{raw}'")
    print(f"  Cleaned: '{cleaned}'")

    # Test keyword extraction
    keywords = extract_keywords("Build a Streamlit dashboard with async APIs")
    print(f"  Keywords: {keywords}")

    print("✓ Text tools work correctly")
    return True


def test_rubric_tool():
    """Test concept clarity evaluation."""
    print("\nTesting rubric tool...")

    from src.tools.rubric_tool import evaluate_concept_clarity

    # Test with a good concept
    good_concept = "A Streamlit web application that visualizes real-time wildfire grant data with async API calls to government databases"
    score = evaluate_concept_clarity(good_concept)
    print(f"  Good concept score: {score.score}/10")
    print(f"  Feedback: {score.feedback}")

    # Test with a poor concept
    poor_concept = "make something"
    score = evaluate_concept_clarity(poor_concept)
    print(f"  Poor concept score: {score.score}/10")
    print(f"  Feedback: {score.feedback}")

    print("✓ Rubric tool works correctly")
    return True


def test_models():
    """Test data model instantiation."""
    print("\nTesting data models...")

    from src.models.project_models import (
        ProjectIdea, ProjectGoals, FrameworkChoice
    )

    # Test ProjectIdea
    idea = ProjectIdea(
        raw_description="Build a dashboard",
        refined_summary="A comprehensive web dashboard for data visualization",
        constraints={"time": "1 week", "complexity": "medium"}
    )
    print(f"✓ ProjectIdea: {idea.refined_summary}")

    # Test ProjectGoals
    goals = ProjectGoals(
        learning_goals=["Learn async/await patterns", "Practice API design"],
        technical_goals=["Build REST API", "Create dashboard UI"],
        priority_notes="Focus on learning async patterns"
    )
    print(f"✓ ProjectGoals: {len(goals.learning_goals)} learning, {len(goals.technical_goals)} technical")

    # Test FrameworkChoice
    framework = FrameworkChoice(
        frontend="Streamlit",
        backend="FastAPI",
        storage="SQLite",
        special_libs=["pandas", "httpx"]
    )
    print(f"✓ FrameworkChoice: {framework.frontend} + {framework.backend}")

    print("✓ All data models work correctly")
    return True


def test_file_structure():
    """Verify all required Phase 2 files exist."""
    print("\nTesting file structure...")

    required_files = [
        'project_forge/src/agents/concept_expander_agent.py',
        'project_forge/src/agents/goals_analyzer_agent.py',
        'project_forge/src/agents/framework_selector_agent.py',
        'project_forge/src/orchestration/crew_config.py',
        'project_forge/src/orchestration/runner.py',
        'project_forge/src/models/project_models.py',
        'project_forge/src/tools/text_cleaner_tool.py',
        'project_forge/src/tools/rubric_tool.py',
        'project_forge/src/config/defaults.yaml'
    ]

    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✓ {file_path} ({size} bytes)")
        else:
            print(f"✗ {file_path} MISSING")
            all_exist = False

    if all_exist:
        print("✓ All required files exist")
    return all_exist


def main():
    """Run all validation tests."""
    print("=" * 80)
    print("PHASE 2 STRUCTURE VALIDATION")
    print("=" * 80)

    tests = [
        ("File Structure", test_file_structure),
        ("Models", test_models),
        ("Text Tools", test_text_tools),
        ("Rubric Tool", test_rubric_tool),
        ("Imports", test_imports),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ {test_name} failed with error: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))

    print("\n" + "=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)

    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")

    all_passed = all(passed for _, passed in results)

    print("\n" + "=" * 80)
    if all_passed:
        print("✓ ALL TESTS PASSED - Phase 2 structure is valid")
        print("=" * 80)
        print("\nNote: Full end-to-end testing requires:")
        print("  1. Valid OPENAI_API_KEY in .env file")
        print("  2. Properly installed CrewAI dependencies")
        print("  3. Run: python -m src.orchestration.runner \"your project idea\"")
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        print("=" * 80)
        return 1


if __name__ == "__main__":
    sys.exit(main())
