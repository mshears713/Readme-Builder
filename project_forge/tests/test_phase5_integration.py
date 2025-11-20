"""
Phase 5 Integration Tests - Validates model integrity and crew wiring.

This test file provides basic validation that Project Forge components
are properly structured and can be instantiated without errors.

Tests cover:
- Data model integrity (all models can be created)
- Agent creation (all agents can be instantiated)
- Tool functionality (basic tool operations work)
- Configuration loading (defaults.yaml loads correctly)
- Crew wiring (components can be connected)

Teaching Note:
    These are "smoke tests" - they verify basic functionality without
    running expensive LLM operations. They catch import errors, structural
    issues, and missing dependencies quickly.

    For full integration testing, you'd run actual agent crews with test
    inputs, but that's slow and costs API credits. These tests balance
    coverage with speed.
"""

import os
import sys
from pathlib import Path

import pytest

# Add project_forge to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

os.environ.setdefault("OPENAI_API_KEY", "test-key")


class TestModelIntegrity:
    """Test that all data models can be instantiated."""

    def test_project_idea_creation(self):
        """Test ProjectIdea model."""
        from src.models.project_models import ProjectIdea

        idea = ProjectIdea(
            raw_description="Build a habit tracker",
            refined_summary="A comprehensive habit tracking application",
            constraints={"time": "1 week", "skill": "beginner"}
        )

        assert idea.raw_description == "Build a habit tracker"
        assert idea.refined_summary is not None
        assert "time" in idea.constraints

    def test_project_goals_creation(self):
        """Test ProjectGoals model."""
        from src.models.project_models import ProjectGoals

        goals = ProjectGoals(
            learning_goals=["Learn Streamlit", "Understand state management"],
            technical_goals=["Build a web app", "Implement data persistence"],
            priority_notes="Focus on basics"
        )

        assert len(goals.learning_goals) == 2
        assert len(goals.technical_goals) == 2
        assert goals.priority_notes is not None

    def test_framework_choice_creation(self):
        """Test FrameworkChoice model."""
        from src.models.project_models import FrameworkChoice

        framework = FrameworkChoice(
            frontend="Streamlit",
            backend="Python",
            storage="JSON files",
            special_libs=["pandas"]
        )

        assert framework.frontend == "Streamlit"
        assert framework.backend == "Python"
        assert "pandas" in framework.special_libs

    def test_step_creation(self):
        """Test Step model."""
        from src.models.project_models import Step

        step = Step(
            index=1,
            title="Create project structure",
            description="Set up directories and files",
            teaching_guidance="Project organization",
            dependencies=[]
        )

        assert step.index == 1
        assert step.title is not None
        assert step.dependencies == []

    def test_phase_creation(self):
        """Test Phase model."""
        from src.models.project_models import Phase, Step

        step1 = Step(1, "First step", "Description", "Learning", [])
        step2 = Step(2, "Second step", "Description", "Learning", [1])

        phase = Phase(
            index=1,
            name="Foundation",
            description="Set up basics",
            steps=[step1, step2]
        )

        assert phase.index == 1
        assert len(phase.steps) == 2
        assert phase.steps[0].index == 1

    def test_project_plan_creation(self):
        """Test complete ProjectPlan model."""
        from src.models.project_models import (
            ProjectPlan, ProjectIdea, ProjectGoals,
            FrameworkChoice, Phase, Step
        )

        idea = ProjectIdea("raw", "refined", {})
        goals = ProjectGoals(["learn"], ["tech"], "notes")
        framework = FrameworkChoice("Streamlit", "Python", "JSON", [])

        step = Step(1, "Setup", "desc", "learn", [])
        phase = Phase(1, "Phase 1", "desc", [step])

        plan = ProjectPlan(
            idea=idea,
            goals=goals,
            framework=framework,
            phases=[phase],
            teaching_notes="Global notes"
        )

        assert plan.idea == idea
        assert plan.goals == goals
        assert len(plan.phases) == 1
        assert plan.teaching_notes == "Global notes"


class TestAgentCreation:
    """Test that all agents can be instantiated."""

    def test_concept_expander_agent(self):
        """Test ConceptExpanderAgent creation."""
        from src.agents.concept_expander_agent import create_concept_expander_agent

        agent = create_concept_expander_agent()

        assert agent is not None
        assert agent.role is not None
        assert agent.goal is not None

    def test_goals_analyzer_agent(self):
        """Test GoalsAnalyzerAgent creation."""
        from src.agents.goals_analyzer_agent import create_goals_analyzer_agent

        agent = create_goals_analyzer_agent()

        assert agent is not None
        assert agent.role is not None

    def test_framework_selector_agent(self):
        """Test FrameworkSelectorAgent creation."""
        from src.agents.framework_selector_agent import create_framework_selector_agent

        agent = create_framework_selector_agent()

        assert agent is not None
        assert agent.role is not None

    def test_phase_designer_agent(self):
        """Test PhaseDesignerAgent creation."""
        from src.agents.phase_designer_agent import create_phase_designer_agent

        agent = create_phase_designer_agent()

        assert agent is not None
        assert agent.role is not None

    def test_teacher_agent(self):
        """Test TeacherAgent creation."""
        from src.agents.teacher_agent import create_teacher_agent

        agent = create_teacher_agent()

        assert agent is not None
        assert agent.role is not None

    def test_evaluator_agent(self):
        """Test EvaluatorAgent creation."""
        from src.agents.evaluator_agent import create_evaluator_agent

        agent = create_evaluator_agent()

        assert agent is not None
        assert agent.role is not None

    def test_prd_writer_agent(self):
        """Test PRDWriterAgent creation."""
        from src.agents.prd_writer_agent import create_prd_writer_agent

        agent = create_prd_writer_agent()

        assert agent is not None
        assert agent.role is not None


class TestToolFunctionality:
    """Test that tools work correctly."""

    def test_evaluate_concept_clarity(self):
        """Test concept clarity evaluation."""
        from src.tools.rubric_tool import evaluate_concept_clarity, RubricCriterion

        score = evaluate_concept_clarity("Build a comprehensive Streamlit dashboard for tracking habits")

        assert score.criterion == RubricCriterion.CLARITY
        assert 0 <= score.score <= 10
        assert score.feedback is not None

    def test_evaluate_phase_balance(self):
        """Test phase balance evaluation."""
        from src.tools.rubric_tool import evaluate_phase_balance
        from src.models.project_models import Phase, Step

        # Create balanced phases
        phases = []
        for i in range(5):
            steps = [Step(j, f"Step {j}", "desc", "learn", []) for j in range(10)]
            phases.append(Phase(i+1, f"Phase {i+1}", "desc", steps))

        score = evaluate_phase_balance(phases)

        assert 0 <= score.score <= 10
        assert score.feedback is not None

    def test_validate_project_plan(self):
        """Test project plan consistency validation."""
        from src.tools.consistency_tool import validate_project_plan
        from src.models.project_models import (
            ProjectPlan, ProjectIdea, ProjectGoals,
            FrameworkChoice, Phase, Step
        )

        idea = ProjectIdea("raw", "refined idea", {})
        goals = ProjectGoals(["learn"], ["tech"], "notes")
        framework = FrameworkChoice("Streamlit", "Python", "JSON", [])

        step = Step(1, "Setup", "description", "learning", [])
        phase = Phase(1, "Phase 1", "description", [step])

        plan = ProjectPlan(idea, goals, framework, [phase], "notes")

        report = validate_project_plan(plan)

        assert report is not None
        assert hasattr(report, 'has_errors')
        assert hasattr(report, 'summary')


class TestConfigurationLoading:
    """Test that configuration files load correctly."""

    def test_load_defaults_yaml(self):
        """Test defaults.yaml loads without errors."""
        import yaml
        from pathlib import Path

        config_path = Path(__file__).parent.parent / "src" / "config" / "defaults.yaml"

        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        assert config is not None
        assert "skill_levels" in config
        assert "project_defaults" in config
        assert "framework_templates" in config

    def test_skill_levels_config(self):
        """Test skill level configurations are complete."""
        import yaml
        from pathlib import Path

        config_path = Path(__file__).parent.parent / "src" / "config" / "defaults.yaml"

        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        skill_levels = config["skill_levels"]

        assert "beginner" in skill_levels
        assert "intermediate" in skill_levels
        assert "advanced" in skill_levels

        # Check beginner has required fields
        beginner = skill_levels["beginner"]
        assert "description" in beginner
        assert "preferred_frameworks" in beginner
        assert "max_complexity" in beginner

    def test_project_types_config(self):
        """Test project type configurations."""
        import yaml
        from pathlib import Path

        config_path = Path(__file__).parent.parent / "src" / "config" / "defaults.yaml"

        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        project_types = config.get("project_types", {})

        assert "toy" in project_types
        assert "medium" in project_types
        assert "ambitious" in project_types

        # Check toy project config
        toy = project_types["toy"]
        assert "recommended_phases" in toy
        assert "recommended_steps" in toy


class TestCrewWiring:
    """Test that crew components can be wired together."""

    def test_planning_crew_structure(self):
        """Test planning crew has correct structure."""
        # This test verifies imports work without executing expensive operations
        from src.orchestration import crew_config

        assert hasattr(crew_config, 'create_planning_crew')
        assert callable(crew_config.create_planning_crew)

    def test_full_plan_crew_structure(self):
        """Test full plan crew has correct structure."""
        from src.orchestration import crew_config

        assert hasattr(crew_config, 'create_full_plan_crew')
        assert callable(crew_config.create_full_plan_crew)

    def test_complete_pipeline_structure(self):
        """Test complete pipeline has correct structure."""
        from src.orchestration import crew_config

        assert hasattr(crew_config, 'create_complete_pipeline')
        assert callable(crew_config.create_complete_pipeline)


class TestRubricSystem:
    """Test Phase 5 enhanced rubric system."""

    def test_all_rubrics_available(self):
        """Test all rubric criteria are defined."""
        from src.tools.rubric_tool import (
            get_all_rubrics,
            RubricCriterion
        )

        rubrics = get_all_rubrics()

        assert RubricCriterion.CLARITY in rubrics
        assert RubricCriterion.FEASIBILITY in rubrics
        assert RubricCriterion.TEACHING_VALUE in rubrics
        assert RubricCriterion.TECHNICAL_DEPTH in rubrics
        assert RubricCriterion.COMPLETENESS in rubrics
        assert RubricCriterion.BALANCE in rubrics

    def test_teaching_clarity_evaluation(self):
        """Test enhanced teaching clarity evaluation."""
        from src.tools.rubric_tool import evaluate_teaching_clarity
        from src.models.project_models import (
            ProjectPlan, ProjectIdea, ProjectGoals,
            FrameworkChoice, Phase, Step
        )

        # Create a plan with good teaching notes
        idea = ProjectIdea("raw", "refined", {})
        goals = ProjectGoals(["learn"], ["tech"], "notes")
        framework = FrameworkChoice("Streamlit", "Python", "JSON", [])

        steps = []
        for i in range(10):
            step = Step(
                i+1,
                f"Step {i+1}",
                "description",
                "This step teaches you about important concepts and patterns",
                []
            )
            steps.append(step)

        phase = Phase(1, "Foundation", "Basic setup", steps)
        plan = ProjectPlan(idea, goals, framework, [phase], "Comprehensive global teaching notes")

        score = evaluate_teaching_clarity(plan, "intermediate")

        assert 0 <= score.score <= 10
        assert score.feedback is not None

    def test_technical_depth_evaluation(self):
        """Test technical depth evaluation."""
        from src.tools.rubric_tool import evaluate_technical_depth
        from src.models.project_models import (
            ProjectPlan, ProjectIdea, ProjectGoals,
            FrameworkChoice, Phase, Step
        )

        idea = ProjectIdea("raw", "refined", {})
        goals = ProjectGoals(["learn"], ["tech"], "notes")
        framework = FrameworkChoice("FastAPI", "FastAPI", "PostgreSQL", ["pytest", "docker"])

        # Create steps with technical depth indicators
        steps = [
            Step(1, "Set up testing framework", "Add pytest", "Testing", []),
            Step(2, "Implement error handling", "Add try/except", "Error handling", []),
            Step(3, "Add database migrations", "Use Alembic", "Database", []),
            Step(4, "Deploy to production", "Use Docker", "Deployment", []),
        ]

        phase = Phase(1, "Setup", "desc", steps)
        plan = ProjectPlan(idea, goals, framework, [phase], "notes")

        score = evaluate_technical_depth(plan, "intermediate")

        assert 0 <= score.score <= 10

    def test_feasibility_for_project_type(self):
        """Test feasibility evaluation with project type."""
        from src.tools.rubric_tool import evaluate_feasibility_for_project_type
        from src.models.project_models import (
            ProjectPlan, ProjectIdea, ProjectGoals,
            FrameworkChoice, Phase, Step
        )

        idea = ProjectIdea("raw", "refined", {})
        goals = ProjectGoals(["learn"], ["tech"], "notes")
        framework = FrameworkChoice("Streamlit", "Python", "JSON", [])

        # Create medium-sized project (40 steps)
        phases = []
        for p in range(5):
            steps = [Step(i, f"Step {i}", "desc", "learn", []) for i in range(8)]
            phases.append(Phase(p+1, f"Phase {p+1}", "desc", steps))

        plan = ProjectPlan(idea, goals, framework, phases, "notes")

        # Test for medium project type
        score = evaluate_feasibility_for_project_type(plan, "medium", "1-2 weeks")

        assert 0 <= score.score <= 10


class TestRunnerCLI:
    """Test runner CLI argument parsing."""

    def test_parse_arguments_function_exists(self):
        """Test parse_arguments function exists."""
        from src.orchestration import runner

        assert hasattr(runner, 'parse_arguments')
        assert callable(runner.parse_arguments)

    def test_runner_main_function_exists(self):
        """Test main function exists."""
        from src.orchestration import runner

        assert hasattr(runner, 'main')
        assert callable(runner.main)


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
