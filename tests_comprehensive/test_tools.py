"""
Test suite for Project Forge tools.

Tests text_cleaner_tool, rubric_tool, and consistency_tool to ensure
they provide correct utility functions for the agents.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from project_forge.src.tools.text_cleaner_tool import (
    clean_project_idea,
    normalize_whitespace,
    remove_filler_words,
    expand_common_abbreviations,
    extract_keywords
)
from project_forge.src.tools.rubric_tool import (
    RubricCriterion,
    RubricScore,
    evaluate_concept_clarity,
    evaluate_phase_balance,
    evaluate_teaching_clarity
)
from project_forge.src.tools.consistency_tool import (
    check_phase_count,
    check_step_numbering,
    check_dependencies,
    ConsistencyReport
    check_phase_count,
    check_step_count,
    check_step_numbering
)
from project_forge.src.models.project_models import (
    ProjectIdea,
    ProjectPlan,
    ProjectGoals,
    FrameworkChoice,
    Phase,
    Step
)


# ============================================================================
# TEXT CLEANER TOOL TESTS
# ============================================================================

def test_clean_project_idea_basic():
    """Test basic project idea cleaning."""
    print("Testing basic project idea cleaning...")

    text = "  Build   a   todo  app  "
    cleaned = clean_project_idea(text)

    assert "Build" in cleaned
    assert "todo" in cleaned or "application" in cleaned
    assert "   " not in cleaned  # No triple spaces
    print("✓ Basic project idea cleaning works")


def test_clean_project_idea_with_fillers():
    """Test cleaning project idea with filler words."""
    print("Testing cleaning with filler words...")

    text = "Um, I want to like build a dashboard"
    cleaned = clean_project_idea(text)

    assert "Um" not in cleaned
    assert "like" not in cleaned
    assert "dashboard" in cleaned
    print("✓ Filler words removal works")


def test_clean_project_idea_abbreviations():
    """Test abbreviation expansion."""
    print("Testing abbreviation expansion...")

    text = "Build a DB with auth"
    cleaned = clean_project_idea(text)

    assert "database" in cleaned.lower()
    assert "authentication" in cleaned.lower()
    print("✓ Abbreviation expansion works")


def test_clean_project_idea_empty():
    """Test cleaning empty string."""
    print("Testing empty string cleaning...")

    text = ""
    cleaned = clean_project_idea(text)

    assert cleaned == ""
    print("✓ Empty string cleaning works")


def test_normalize_whitespace():
    """Test whitespace normalization."""
    print("Testing whitespace normalization...")

    text = "Hello    World\t\tFoo   Bar"
    normalized = normalize_whitespace(text)

    # Should normalize to single spaces
    assert "    " not in normalized
    assert "\t\t" not in normalized
    print("✓ Whitespace normalization works")


def test_extract_keywords():
    """Test keyword extraction."""
    print("Testing keyword extraction...")

    text = "Build a Streamlit dashboard with async APIs"
    keywords = extract_keywords(text)

    assert isinstance(keywords, list)
    assert "streamlit" in keywords
    assert "dashboard" in keywords
    assert "async" in keywords
    print(f"  Extracted keywords: {keywords}")
    print("✓ Keyword extraction works")


# ============================================================================
# RUBRIC TOOL TESTS
# ============================================================================

def test_rubric_score_creation():
    """Test creating a RubricScore."""
    print("Testing RubricScore creation...")

    score = RubricScore(
        criterion=RubricCriterion.CLARITY,
        score=8,
        feedback="Good clarity",
        pass_threshold=7
    )

    assert score.criterion == RubricCriterion.CLARITY
    assert score.score == 8
    assert score.passes() == True
    print("✓ RubricScore creation works")


def test_rubric_score_failing():
    """Test failing RubricScore."""
    print("Testing failing RubricScore...")

    score = RubricScore(
        criterion=RubricCriterion.CLARITY,
        score=5,
        feedback="Needs improvement",
        pass_threshold=7
    )

    assert score.passes() == False
    print("✓ Failing RubricScore detection works")


def test_evaluate_concept_clarity_good():
    """Test concept clarity evaluation with good input."""
    print("Testing concept clarity evaluation (good)...")

    idea = ProjectIdea(
        raw_description="Build a task management app",
        refined_summary="A comprehensive task management application with user authentication, "
                       "task categorization, priority levels, and deadline tracking. "
                       "Built for intermediate developers to learn REST APIs and database design.",
        constraints={"time": "2 weeks", "skill": "intermediate", "complexity": "medium"}
    )

    score = evaluate_concept_clarity(idea.refined_summary)

    assert isinstance(score, RubricScore)
    assert score.criterion == RubricCriterion.CLARITY
    assert score.score >= 7  # Should be good clarity
    print(f"  Score: {score.score}/10 - {score.feedback}")
    print("✓ Good concept clarity evaluation works")


def test_evaluate_concept_clarity_poor():
    """Test concept clarity evaluation with poor input."""
    print("Testing concept clarity evaluation (poor)...")

    idea = ProjectIdea(
        raw_description="Build something",
        refined_summary="An app",
        constraints={}
    )

    score = evaluate_concept_clarity(idea.refined_summary)

    assert isinstance(score, RubricScore)
    assert score.score < 7  # Should be poor clarity
    print(f"  Score: {score.score}/10 - {score.feedback}")
    print("✓ Poor concept clarity evaluation works")


def test_evaluate_phase_balance_good():
    """Test phase balance evaluation with balanced phases."""
    print("Testing phase balance evaluation (good)...")

    phases = []
    for i in range(1, 6):
        steps = [Step(index=j, title=f"Step {j}") for j in range((i-1)*10+1, i*10+1)]
        phases.append(Phase(
            index=i,
            name=f"Phase {i}",
            description=f"This is phase {i} with meaningful description",
            steps=steps
        ))

    score = evaluate_phase_balance(phases)

    assert isinstance(score, RubricScore)
    assert score.criterion == RubricCriterion.BALANCE
    assert score.score >= 7  # Should be well-balanced
    print(f"  Score: {score.score}/10 - {score.feedback}")
    print("✓ Good phase balance evaluation works")


def test_evaluate_phase_balance_poor():
    """Test phase balance evaluation with unbalanced phases."""
    print("Testing phase balance evaluation (poor)...")

    phases = [
        Phase(index=1, name="Phase 1", description="", steps=[Step(index=1, title="S1")]),
        Phase(index=2, name="Phase 2", description="", steps=[
            Step(index=i, title=f"S{i}") for i in range(2, 22)
        ]),
        Phase(index=3, name="Phase 3", description="", steps=[]),
    ]

    score = evaluate_phase_balance(phases)

    assert isinstance(score, RubricScore)
    assert score.score < 7  # Should be poorly balanced
    print(f"  Score: {score.score}/10 - {score.feedback}")
    print("✓ Poor phase balance evaluation works")


def test_evaluate_teaching_clarity_good():
    """Test teaching quality evaluation with good annotations."""
    print("Testing teaching quality evaluation (good)...")

    idea = ProjectIdea(raw_description="Learn Python")
    goals = ProjectGoals(learning_goals=["Learn async", "Learn testing"])
    framework = FrameworkChoice()

    steps = []
    for i in range(1, 21):
        steps.append(Step(
            index=i,
            title=f"Step {i}",
            description=f"Implement feature {i}",
            what_you_learn=f"In this step you'll learn about important concept {i} and why it matters for your development"
        ))

    phases = [
        Phase(index=1, name="Phase 1", steps=steps[:10]),
        Phase(index=2, name="Phase 2", steps=steps[10:])
    ]

    plan = ProjectPlan(
        idea=idea,
        goals=goals,
        framework=framework,
        phases=phases,
        teaching_notes="This project teaches you fundamental concepts in a progressive manner"
    )

    score = evaluate_teaching_clarity(plan)

    assert isinstance(score, RubricScore)
    assert score.criterion == RubricCriterion.TEACHING_VALUE
    assert score.score >= 7  # Should have good teaching quality
    print(f"  Score: {score.score}/10 - {score.feedback}")
    print("✓ Good teaching quality evaluation works")


def test_evaluate_teaching_clarity_poor():
    """Test teaching quality evaluation with missing annotations."""
    print("Testing teaching quality evaluation (poor)...")

    idea = ProjectIdea(raw_description="Build app")
    goals = ProjectGoals()
    framework = FrameworkChoice()

    steps = [Step(index=i, title=f"Step {i}") for i in range(1, 11)]
    phases = [Phase(index=1, name="Phase 1", steps=steps)]

    plan = ProjectPlan(
        idea=idea,
        goals=goals,
        framework=framework,
        phases=phases
    )

    score = evaluate_teaching_clarity(plan)

    assert isinstance(score, RubricScore)
    assert score.score < 7  # Should have poor teaching quality
    print(f"  Score: {score.score}/10 - {score.feedback}")
    print("✓ Poor teaching quality evaluation works")


# ============================================================================
# CONSISTENCY TOOL TESTS
# ============================================================================

def test_check_phase_count_correct():
    """Test phase count validation with correct count."""
    print("Testing phase count validation (correct)...")

    phases = [Phase(index=i, name=f"Phase {i}") for i in range(1, 6)]

    is_valid, message = check_phase_count(phases)

    assert is_valid == True
    assert "5 phases" in message
    print(f"  {message}")
    print("✓ Correct phase count validation works")


def test_check_phase_count_incorrect():
    """Test phase count validation with incorrect count."""
    print("Testing phase count validation (incorrect)...")

    phases = [Phase(index=i, name=f"Phase {i}") for i in range(1, 4)]

    is_valid, message = check_phase_count(phases)

    assert is_valid == False
    assert "3 phases" in message or "not 5" in message.lower()
    print(f"  {message}")
    print("✓ Incorrect phase count validation works")


def test_check_step_count_good():
    """Test step count validation with good count."""
    print("Testing step count validation (good)...")

    steps = [Step(index=i, title=f"Step {i}") for i in range(1, 51)]
    phases = [
        Phase(index=1, name="P1", steps=steps[:10]),
        Phase(index=2, name="P2", steps=steps[10:20]),
        Phase(index=3, name="P3", steps=steps[20:30]),
        Phase(index=4, name="P4", steps=steps[30:40]),
        Phase(index=5, name="P5", steps=steps[40:50])
    ]

    is_valid, message = check_step_count(phases)

    assert is_valid == True
    assert "50 total steps" in message
    print(f"  {message}")
    print("✓ Good step count validation works")


def test_check_step_count_too_few():
    """Test step count validation with too few steps."""
    print("Testing step count validation (too few)...")

    steps = [Step(index=i, title=f"Step {i}") for i in range(1, 21)]
    phases = [Phase(index=1, name="P1", steps=steps)]

    is_valid, message = check_step_count(phases)

    assert is_valid == False
    print(f"  {message}")
    print("✓ Too few steps validation works")


def test_check_step_numbering_sequential():
    """Test step index validation with sequential indices."""
    print("Testing step index validation (sequential)...")

    steps = [Step(index=i, title=f"Step {i}") for i in range(1, 11)]
    phases = [Phase(index=1, name="P1", steps=steps)]

    is_valid, message = check_step_numbering(phases)

    assert is_valid == True
    print(f"  {message}")
    print("✓ Sequential step indices validation works")


def test_check_step_numbering_duplicates():
    """Test step index validation with duplicate indices."""
    print("Testing step index validation (duplicates)...")

    steps = [
        Step(index=1, title="Step 1"),
        Step(index=2, title="Step 2"),
        Step(index=2, title="Step 2 duplicate"),  # Duplicate!
        Step(index=3, title="Step 3")
    ]
    phases = [Phase(index=1, name="P1", steps=steps)]

    is_valid, message = check_step_numbering(phases)

    assert is_valid == False
    assert "duplicate" in message.lower()
    print(f"  {message}")
    print("✓ Duplicate indices detection works")


def test_check_step_numbering_gaps():
    """Test step index validation with gaps."""
    print("Testing step index validation (gaps)...")

    steps = [
        Step(index=1, title="Step 1"),
        Step(index=2, title="Step 2"),
        Step(index=5, title="Step 5"),  # Gap: missing 3, 4
        Step(index=6, title="Step 6")
    ]
    phases = [Phase(index=1, name="P1", steps=steps)]

    is_valid, message = check_step_numbering(phases)

    assert is_valid == False
    assert "gap" in message.lower() or "missing" in message.lower()
    print(f"  {message}")
    print("✓ Index gaps detection works")


def run_all_tests():
    """Run all tool tests."""
    print("\n" + "=" * 60)
    print("RUNNING TOOLS TESTS")
    print("=" * 60 + "\n")

    try:
        # Text Cleaner Tests
        print("\n--- Text Cleaner Tool Tests ---\n")
        test_clean_project_idea_basic()
        test_clean_project_idea_with_fillers()
        test_clean_project_idea_abbreviations()
        test_clean_project_idea_empty()
        test_normalize_whitespace()
        test_extract_keywords()

        # Rubric Tool Tests
        print("\n--- Rubric Tool Tests ---\n")
        test_rubric_score_creation()
        test_rubric_score_failing()
        test_evaluate_concept_clarity_good()
        test_evaluate_concept_clarity_poor()
        test_evaluate_phase_balance_good()
        test_evaluate_phase_balance_poor()
        test_evaluate_teaching_clarity_good()
        test_evaluate_teaching_clarity_poor()

        # Consistency Tool Tests
        print("\n--- Consistency Tool Tests ---\n")
        test_check_phase_count_correct()
        test_check_phase_count_incorrect()
        test_check_step_count_good()
        test_check_step_count_too_few()
        test_check_step_numbering_sequential()
        test_check_step_numbering_duplicates()
        test_check_step_numbering_gaps()

        print("\n" + "=" * 60)
        print("✓ ALL TOOLS TESTS PASSED")
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
