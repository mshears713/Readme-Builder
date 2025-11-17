"""
Simplified but comprehensive system health test.

This test verifies that all core components can be imported, instantiated,
and basic operations work correctly without making actual API calls.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_all_imports():
    """Test that all modules can be imported without errors."""
    print("Testing all imports...")

    try:
        # Data models
        from project_forge.src.models.project_models import (
            ProjectIdea, ProjectGoals, FrameworkChoice, Step, Phase, ProjectPlan
        )

        # Tools
        from project_forge.src.tools.text_cleaner_tool import (
            clean_project_idea, normalize_whitespace, extract_keywords
        )
        from project_forge.src.tools.rubric_tool import (
            RubricCriterion, RubricScore, evaluate_concept_clarity, evaluate_phase_balance
        )
        from project_forge.src.tools.consistency_tool import (
            check_phase_count, check_step_numbering, validate_project_plan
        )

        # Agents
        from project_forge.src.agents.concept_expander_agent import create_concept_expander_agent
        from project_forge.src.agents.goals_analyzer_agent import create_goals_analyzer_agent
        from project_forge.src.agents.framework_selector_agent import create_framework_selector_agent
        from project_forge.src.agents.phase_designer_agent import create_phase_designer_agent
        from project_forge.src.agents.teacher_agent import create_teacher_agent
        from project_forge.src.agents.prd_writer_agent import create_prd_writer_agent

        # Orchestration
        from project_forge.src.orchestration.runner import parse_arguments, setup_logging
        from project_forge.src.orchestration.crew_config import PlanningResult

        print("✓ All modules imported successfully")
        return True

    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def test_data_model_creation():
    """Test creating all data model objects."""
    print("Testing data model creation...")

    from project_forge.src.models.project_models import (
        ProjectIdea, ProjectGoals, FrameworkChoice, Step, Phase, ProjectPlan
    )

    # Create all models
    idea = ProjectIdea(raw_description="Test")
    goals = ProjectGoals(learning_goals=["Test"])
    framework = FrameworkChoice(frontend="Streamlit")
    step = Step(index=1, title="Test Step")
    phase = Phase(index=1, name="Test Phase", steps=[step])
    plan = ProjectPlan(idea=idea, goals=goals, framework=framework, phases=[phase])

    assert idea is not None
    assert goals is not None
    assert framework is not None
    assert step is not None
    assert phase is not None
    assert plan is not None
    assert len(plan.phases) == 1
    assert plan.phases[0].steps[0].title == "Test Step"

    print("✓ All data models created successfully")
    return True


def test_tools_basic_operations():
    """Test basic tool operations."""
    print("Testing tools basic operations...")

    from project_forge.src.tools.text_cleaner_tool import clean_project_idea, extract_keywords
    from project_forge.src.tools.rubric_tool import evaluate_concept_clarity, RubricScore
    from project_forge.src.tools.consistency_tool import check_phase_count
    from project_forge.src.models.project_models import Phase

    # Text cleaner
    cleaned = clean_project_idea("  Test   idea  ")
    assert "Test" in cleaned
    assert "idea" in cleaned or "Idea" in cleaned

    keywords = extract_keywords("Build a Streamlit dashboard")
    assert isinstance(keywords, list)

    # Rubric tool
    score = evaluate_concept_clarity("A detailed project to build a comprehensive app with features")
    assert isinstance(score, RubricScore)
    assert 0 <= score.score <= 10

    # Consistency tool
    phases = [Phase(index=i, name=f"Phase {i}") for i in range(1, 6)]
    report = check_phase_count(phases)
    assert report.passed == True

    print("✓ All tools work correctly")
    return True


def test_agent_creation():
    """Test creating all agents."""
    print("Testing agent creation...")

    from project_forge.src.agents.concept_expander_agent import create_concept_expander_agent
    from project_forge.src.agents.goals_analyzer_agent import create_goals_analyzer_agent
    from project_forge.src.agents.framework_selector_agent import create_framework_selector_agent
    from project_forge.src.agents.phase_designer_agent import create_phase_designer_agent
    from project_forge.src.agents.teacher_agent import create_teacher_agent
    from project_forge.src.agents.prd_writer_agent import create_prd_writer_agent

    agents = [
        create_concept_expander_agent(),
        create_goals_analyzer_agent(),
        create_framework_selector_agent(),
        create_phase_designer_agent(),
        create_teacher_agent(),
        create_prd_writer_agent()
    ]

    for agent in agents:
        assert agent is not None
        assert hasattr(agent, 'role')
        assert hasattr(agent, 'goal')
        assert hasattr(agent, 'backstory')

    print("✓ All 7 agents created successfully")
    return True


def test_cli_argument_parsing():
    """Test CLI argument parsing."""
    print("Testing CLI argument parsing...")

    from project_forge.src.orchestration.runner import parse_arguments
    import sys

    # Save original argv
    original_argv = sys.argv

    try:
        # Test basic parsing
        sys.argv = ["runner.py", "Test project"]
        args = parse_arguments()
        assert args.idea == "Test project"
        assert args.skill == "intermediate"

        # Test with options
        sys.argv = ["runner.py", "--skill", "beginner", "--phase", "2", "Test"]
        args = parse_arguments()
        assert args.skill == "beginner"
        assert args.phase == 2

        print("✓ CLI argument parsing works")
        return True

    finally:
        # Restore original argv
        sys.argv = original_argv


def test_complete_data_flow():
    """Test that data flows correctly through the models."""
    print("Testing complete data flow...")

    from project_forge.src.models.project_models import (
        ProjectIdea, ProjectGoals, FrameworkChoice, Step, Phase, ProjectPlan
    )

    # Create a complete plan
    idea = ProjectIdea(
        raw_description="Build a todo app",
        refined_summary="A task management application",
        constraints={"skill": "beginner"}
    )

    goals = ProjectGoals(
        learning_goals=["Learn Python", "Learn databases"],
        technical_goals=["Build CRUD app", "Add authentication"]
    )

    framework = FrameworkChoice(
        frontend="Streamlit",
        backend="FastAPI",
        storage="SQLite"
    )

    # Create 5 phases with 10 steps each
    phases = []
    step_index = 1
    for phase_num in range(1, 6):
        steps = []
        for _ in range(10):
            steps.append(Step(
                index=step_index,
                title=f"Step {step_index}",
                description=f"Implement feature {step_index}",
                what_you_learn=f"Learn concept {step_index}"
            ))
            step_index += 1

        phases.append(Phase(
            index=phase_num,
            name=f"Phase {phase_num}",
            description=f"Complete phase {phase_num}",
            steps=steps
        ))

    plan = ProjectPlan(
        idea=idea,
        goals=goals,
        framework=framework,
        phases=phases,
        teaching_notes="This is a teaching project"
    )

    # Verify structure
    assert len(plan.phases) == 5
    assert sum(len(p.steps) for p in plan.phases) == 50
    assert plan.idea.raw_description == "Build a todo app"
    assert len(plan.goals.learning_goals) == 2
    assert plan.framework.frontend == "Streamlit"
    assert plan.teaching_notes != ""

    # Verify step indices are correct
    all_indices = [step.index for phase in plan.phases for step in phase.steps]
    assert all_indices == list(range(1, 51))

    print("✓ Complete data flow works correctly")
    return True


def test_consistency_validation():
    """Test consistency validation on a valid plan."""
    print("Testing consistency validation...")

    from project_forge.src.models.project_models import ProjectIdea, ProjectGoals, FrameworkChoice, Step, Phase, ProjectPlan
    from project_forge.src.tools.consistency_tool import validate_project_plan

    # Create a valid plan
    idea = ProjectIdea(raw_description="Test")
    goals = ProjectGoals()
    framework = FrameworkChoice()

    steps = [Step(index=i, title=f"Step {i}") for i in range(1, 11)]
    phases = [
        Phase(index=1, name="P1", steps=steps[:2]),
        Phase(index=2, name="P2", steps=steps[2:4]),
        Phase(index=3, name="P3", steps=steps[4:6]),
        Phase(index=4, name="P4", steps=steps[6:8]),
        Phase(index=5, name="P5", steps=steps[8:10])
    ]

    plan = ProjectPlan(idea=idea, goals=goals, framework=framework, phases=phases)

    # Validate
    report = validate_project_plan(plan)
    assert report is not None
    assert report.passed == True
    assert report.get_error_count() == 0

    print("✓ Consistency validation works")
    return True


def test_rubric_evaluations():
    """Test various rubric evaluations."""
    print("Testing rubric evaluations...")

    from project_forge.src.models.project_models import ProjectIdea, ProjectGoals, FrameworkChoice, Step, Phase, ProjectPlan
    from project_forge.src.tools.rubric_tool import evaluate_concept_clarity, evaluate_phase_balance, evaluate_teaching_clarity

    # Test concept clarity
    good_concept = "A comprehensive task management application with user authentication and real-time sync"
    score = evaluate_concept_clarity(good_concept)
    assert score.score >= 7

    # Test phase balance
    steps = [Step(index=i, title=f"Step {i}") for i in range(1, 51)]
    phases = [
        Phase(index=1, name="P1", steps=steps[:10]),
        Phase(index=2, name="P2", steps=steps[10:20]),
        Phase(index=3, name="P3", steps=steps[20:30]),
        Phase(index=4, name="P4", steps=steps[30:40]),
        Phase(index=5, name="P5", steps=steps[40:50])
    ]
    score = evaluate_phase_balance(phases)
    assert score.score >= 7

    # Test teaching clarity
    idea = ProjectIdea(raw_description="Test")
    goals = ProjectGoals()
    framework = FrameworkChoice()

    for step in steps:
        step.what_you_learn = "You will learn about important concepts and why they matter"

    plan = ProjectPlan(
        idea=idea,
        goals=goals,
        framework=framework,
        phases=phases,
        teaching_notes="This project provides a comprehensive learning experience" * 5
    )

    score = evaluate_teaching_clarity(plan)
    assert score.score >= 6  # Should pass with all learning annotations

    print("✓ All rubric evaluations work")
    return True


def run_all_tests():
    """Run all system health tests."""
    print("\n" + "=" * 60)
    print("RUNNING SYSTEM HEALTH TESTS")
    print("=" * 60 + "\n")

    tests = [
        test_all_imports,
        test_data_model_creation,
        test_tools_basic_operations,
        test_agent_creation,
        test_cli_argument_parsing,
        test_complete_data_flow,
        test_consistency_validation,
        test_rubric_evaluations
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} failed with error: {e}")
            import traceback
            traceback.print_exc()
            failed += 1

    print("\n" + "=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60 + "\n")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
