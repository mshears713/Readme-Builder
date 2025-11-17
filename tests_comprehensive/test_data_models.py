"""
Test suite for Project Forge data models.

Tests all dataclasses in project_models.py to ensure they work correctly
and can handle various data scenarios.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from project_forge.src.models.project_models import (
    ProjectIdea,
    ProjectGoals,
    FrameworkChoice,
    Step,
    Phase,
    ProjectPlan
)
import json


def test_project_idea_creation():
    """Test creating a ProjectIdea with minimal data."""
    print("Testing ProjectIdea creation...")

    idea = ProjectIdea(raw_description="Build a todo app")
    assert idea.raw_description == "Build a todo app"
    assert idea.refined_summary == ""
    assert isinstance(idea.constraints, dict)
    assert len(idea.constraints) == 0

    print("✓ ProjectIdea creation works")


def test_project_idea_with_data():
    """Test ProjectIdea with all fields populated."""
    print("Testing ProjectIdea with full data...")

    idea = ProjectIdea(
        raw_description="Build a todo app",
        refined_summary="A simple task management application",
        constraints={"time": "1 week", "skill": "beginner", "complexity": "low"}
    )

    assert idea.raw_description == "Build a todo app"
    assert idea.refined_summary == "A simple task management application"
    assert idea.constraints["time"] == "1 week"
    assert idea.constraints["skill"] == "beginner"
    assert len(idea.constraints) == 3

    print("✓ ProjectIdea with full data works")


def test_project_goals_creation():
    """Test creating ProjectGoals."""
    print("Testing ProjectGoals creation...")

    goals = ProjectGoals()
    assert isinstance(goals.learning_goals, list)
    assert isinstance(goals.technical_goals, list)
    assert len(goals.learning_goals) == 0
    assert len(goals.technical_goals) == 0

    print("✓ ProjectGoals creation works")


def test_project_goals_with_data():
    """Test ProjectGoals with goals added."""
    print("Testing ProjectGoals with data...")

    goals = ProjectGoals(
        learning_goals=["Learn async programming", "Understand MVC pattern"],
        technical_goals=["Build REST API", "Implement database"],
        priority_notes="Focus on learning async first"
    )

    assert len(goals.learning_goals) == 2
    assert len(goals.technical_goals) == 2
    assert "async" in goals.learning_goals[0]
    assert goals.priority_notes != ""

    print("✓ ProjectGoals with data works")


def test_framework_choice_all_none():
    """Test FrameworkChoice for CLI-only project."""
    print("Testing FrameworkChoice with all None...")

    framework = FrameworkChoice()
    assert framework.frontend is None
    assert framework.backend is None
    assert framework.storage is None
    assert isinstance(framework.special_libs, list)
    assert len(framework.special_libs) == 0

    print("✓ FrameworkChoice with None values works")


def test_framework_choice_with_data():
    """Test FrameworkChoice with full stack."""
    print("Testing FrameworkChoice with full data...")

    framework = FrameworkChoice(
        frontend="Streamlit",
        backend="FastAPI",
        storage="SQLite",
        special_libs=["CrewAI", "LangChain"]
    )

    assert framework.frontend == "Streamlit"
    assert framework.backend == "FastAPI"
    assert framework.storage == "SQLite"
    assert len(framework.special_libs) == 2
    assert "CrewAI" in framework.special_libs

    print("✓ FrameworkChoice with full data works")


def test_step_creation():
    """Test creating a Step."""
    print("Testing Step creation...")

    step = Step(
        index=1,
        title="Create project structure"
    )

    assert step.index == 1
    assert step.title == "Create project structure"
    assert step.description == ""
    assert step.what_you_learn == ""
    assert isinstance(step.dependencies, list)
    assert len(step.dependencies) == 0

    print("✓ Step creation works")


def test_step_with_dependencies():
    """Test Step with dependencies."""
    print("Testing Step with dependencies...")

    step = Step(
        index=5,
        title="Add user authentication",
        description="Implement JWT-based auth",
        what_you_learn="Learn about JWT tokens and session management",
        dependencies=[1, 2, 3]
    )

    assert step.index == 5
    assert len(step.dependencies) == 3
    assert 1 in step.dependencies
    assert step.what_you_learn != ""

    print("✓ Step with dependencies works")


def test_phase_creation():
    """Test creating a Phase."""
    print("Testing Phase creation...")

    phase = Phase(
        index=1,
        name="Foundation",
        description="Set up project structure"
    )

    assert phase.index == 1
    assert phase.name == "Foundation"
    assert isinstance(phase.steps, list)
    assert len(phase.steps) == 0

    print("✓ Phase creation works")


def test_phase_with_steps():
    """Test Phase containing multiple steps."""
    print("Testing Phase with steps...")

    steps = [
        Step(index=1, title="Step 1"),
        Step(index=2, title="Step 2"),
        Step(index=3, title="Step 3")
    ]

    phase = Phase(
        index=1,
        name="Foundation",
        description="Set up project",
        steps=steps
    )

    assert len(phase.steps) == 3
    assert phase.steps[0].index == 1
    assert phase.steps[2].title == "Step 3"

    print("✓ Phase with steps works")


def test_project_plan_creation():
    """Test creating a complete ProjectPlan."""
    print("Testing ProjectPlan creation...")

    idea = ProjectIdea(raw_description="Test project")
    goals = ProjectGoals()
    framework = FrameworkChoice()

    plan = ProjectPlan(
        idea=idea,
        goals=goals,
        framework=framework
    )

    assert plan.idea is not None
    assert plan.goals is not None
    assert plan.framework is not None
    assert isinstance(plan.phases, list)
    assert len(plan.phases) == 0
    assert plan.teaching_notes == ""

    print("✓ ProjectPlan creation works")


def test_project_plan_with_phases():
    """Test ProjectPlan with all 5 phases."""
    print("Testing ProjectPlan with 5 phases...")

    idea = ProjectIdea(raw_description="Test project")
    goals = ProjectGoals(learning_goals=["Learn Python"])
    framework = FrameworkChoice(frontend="Streamlit")

    phases = [
        Phase(index=i, name=f"Phase {i}", description=f"Description {i}")
        for i in range(1, 6)
    ]

    plan = ProjectPlan(
        idea=idea,
        goals=goals,
        framework=framework,
        phases=phases,
        teaching_notes="This is a teaching project"
    )

    assert len(plan.phases) == 5
    assert plan.phases[0].index == 1
    assert plan.phases[4].index == 5
    assert plan.teaching_notes != ""

    print("✓ ProjectPlan with 5 phases works")


def test_nested_data_integrity():
    """Test that nested models maintain data integrity."""
    print("Testing nested data integrity...")

    # Create a complete nested structure
    steps = [
        Step(index=i, title=f"Step {i}", description=f"Do task {i}")
        for i in range(1, 11)
    ]

    phases = [
        Phase(index=1, name="Phase 1", steps=steps[:5]),
        Phase(index=2, name="Phase 2", steps=steps[5:])
    ]

    idea = ProjectIdea(
        raw_description="Complex project",
        refined_summary="A complex multi-phase project"
    )

    goals = ProjectGoals(
        learning_goals=["Goal 1", "Goal 2"],
        technical_goals=["Tech 1", "Tech 2"]
    )

    framework = FrameworkChoice(
        frontend="React",
        backend="Node.js",
        storage="MongoDB"
    )

    plan = ProjectPlan(
        idea=idea,
        goals=goals,
        framework=framework,
        phases=phases
    )

    # Verify all nested data is accessible
    assert plan.idea.refined_summary == "A complex multi-phase project"
    assert len(plan.goals.learning_goals) == 2
    assert plan.framework.backend == "Node.js"
    assert len(plan.phases) == 2
    assert len(plan.phases[0].steps) == 5
    assert plan.phases[1].steps[0].title == "Step 6"

    print("✓ Nested data integrity maintained")


def test_step_count_calculation():
    """Test calculating total steps across all phases."""
    print("Testing step count calculation...")

    phases = []
    step_index = 1

    for phase_num in range(1, 6):
        steps = []
        for _ in range(10):  # 10 steps per phase
            steps.append(Step(index=step_index, title=f"Step {step_index}"))
            step_index += 1
        phases.append(Phase(index=phase_num, name=f"Phase {phase_num}", steps=steps))

    total_steps = sum(len(phase.steps) for phase in phases)
    assert total_steps == 50
    assert step_index == 51  # Next index would be 51

    print("✓ Step count calculation works")


def run_all_tests():
    """Run all data model tests."""
    print("\n" + "=" * 60)
    print("RUNNING DATA MODELS TESTS")
    print("=" * 60 + "\n")

    try:
        test_project_idea_creation()
        test_project_idea_with_data()
        test_project_goals_creation()
        test_project_goals_with_data()
        test_framework_choice_all_none()
        test_framework_choice_with_data()
        test_step_creation()
        test_step_with_dependencies()
        test_phase_creation()
        test_phase_with_steps()
        test_project_plan_creation()
        test_project_plan_with_phases()
        test_nested_data_integrity()
        test_step_count_calculation()

        print("\n" + "=" * 60)
        print("✓ ALL DATA MODEL TESTS PASSED")
        print("=" * 60 + "\n")
        return True

    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}\n")
        return False
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
