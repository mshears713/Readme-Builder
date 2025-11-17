"""
Test suite for basic agent functionality.

Tests that agents can be created and configured correctly.
Does NOT execute agent tasks (to avoid API costs).
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from project_forge.src.agents.concept_expander_agent import create_concept_expander_agent
from project_forge.src.agents.goals_analyzer_agent import create_goals_analyzer_agent
from project_forge.src.agents.framework_selector_agent import create_framework_selector_agent
from project_forge.src.agents.phase_designer_agent import create_phase_designer_agent
from project_forge.src.agents.teacher_agent import create_teacher_agent
from project_forge.src.agents.prd_writer_agent import create_prd_writer_agent


def test_create_concept_expander_agent():
    """Test creating the ConceptExpander agent."""
    print("Testing ConceptExpander agent creation...")

    agent = create_concept_expander_agent()

    assert agent is not None
    assert hasattr(agent, 'role')
    assert hasattr(agent, 'goal')
    assert hasattr(agent, 'backstory')
    assert 'concept' in agent.role.lower() or 'expand' in agent.role.lower()
    print(f"  Agent role: {agent.role}")
    print("✓ ConceptExpander agent created successfully")


def test_create_goals_analyzer_agent():
    """Test creating the GoalsAnalyzer agent."""
    print("Testing GoalsAnalyzer agent creation...")

    agent = create_goals_analyzer_agent()

    assert agent is not None
    assert hasattr(agent, 'role')
    assert hasattr(agent, 'goal')
    assert 'goal' in agent.role.lower() or 'analyz' in agent.role.lower()
    print(f"  Agent role: {agent.role}")
    print("✓ GoalsAnalyzer agent created successfully")


def test_create_framework_selector_agent():
    """Test creating the FrameworkSelector agent."""
    print("Testing FrameworkSelector agent creation...")

    agent = create_framework_selector_agent()

    assert agent is not None
    assert hasattr(agent, 'role')
    assert hasattr(agent, 'goal')
    assert 'framework' in agent.role.lower() or 'stack' in agent.role.lower() or 'technolog' in agent.role.lower()
    print(f"  Agent role: {agent.role}")
    print("✓ FrameworkSelector agent created successfully")


def test_create_phase_designer_agent():
    """Test creating the PhaseDesigner agent."""
    print("Testing PhaseDesigner agent creation...")

    agent = create_phase_designer_agent()

    assert agent is not None
    assert hasattr(agent, 'role')
    assert hasattr(agent, 'goal')
    assert 'phase' in agent.role.lower() or 'design' in agent.role.lower() or 'plan' in agent.role.lower()
    print(f"  Agent role: {agent.role}")
    print("✓ PhaseDesigner agent created successfully")


def test_create_teacher_agent():
    """Test creating the Teacher agent."""
    print("Testing Teacher agent creation...")

    agent = create_teacher_agent()

    assert agent is not None
    assert hasattr(agent, 'role')
    assert hasattr(agent, 'goal')
    assert 'teach' in agent.role.lower() or 'educat' in agent.role.lower() or 'learn' in agent.role.lower()
    print(f"  Agent role: {agent.role}")
    print("✓ Teacher agent created successfully")


def test_create_prd_writer_agent():
    """Test creating the PRDWriter agent."""
    print("Testing PRDWriter agent creation...")

    agent = create_prd_writer_agent()

    assert agent is not None
    assert hasattr(agent, 'role')
    assert hasattr(agent, 'goal')
    assert 'prd' in agent.role.lower() or 'write' in agent.role.lower() or 'readme' in agent.role.lower() or 'document' in agent.role.lower()
    print(f"  Agent role: {agent.role}")
    print("✓ PRDWriter agent created successfully")


def test_all_agents_have_backstory():
    """Test that all agents have meaningful backstories."""
    print("Testing all agents have backstories...")

    agents = [
        create_concept_expander_agent(),
        create_goals_analyzer_agent(),
        create_framework_selector_agent(),
        create_phase_designer_agent(),
        create_teacher_agent(),
        create_prd_writer_agent()
    ]

    for agent in agents:
        assert hasattr(agent, 'backstory')
        assert len(agent.backstory) > 50  # Should be meaningful
        assert isinstance(agent.backstory, str)

    print("✓ All agents have meaningful backstories")


def test_all_agents_have_goals():
    """Test that all agents have clear goals."""
    print("Testing all agents have clear goals...")

    agents = [
        create_concept_expander_agent(),
        create_goals_analyzer_agent(),
        create_framework_selector_agent(),
        create_phase_designer_agent(),
        create_teacher_agent(),
        create_prd_writer_agent()
    ]

    for agent in agents:
        assert hasattr(agent, 'goal')
        assert len(agent.goal) > 20  # Should be meaningful
        assert isinstance(agent.goal, str)

    print("✓ All agents have clear goals")


def test_agent_delegation_settings():
    """Test that agents have appropriate delegation settings."""
    print("Testing agent delegation settings...")

    # Most specialized agents should not delegate
    agents = [
        create_concept_expander_agent(),
        create_goals_analyzer_agent(),
        create_framework_selector_agent(),
        create_phase_designer_agent(),
        create_teacher_agent(),
        create_prd_writer_agent()
    ]

    for agent in agents:
        assert hasattr(agent, 'allow_delegation')
        # For this system, most agents shouldn't delegate
        # (This is a design choice - adjust assertion if needed)

    print("✓ Agent delegation settings are configured")


def test_agent_verbose_settings():
    """Test that agents have verbose mode configured."""
    print("Testing agent verbose settings...")

    agents = [
        create_concept_expander_agent(),
        create_goals_analyzer_agent(),
        create_framework_selector_agent(),
        create_phase_designer_agent(),
        create_teacher_agent(),
        create_prd_writer_agent()
    ]

    for agent in agents:
        assert hasattr(agent, 'verbose')
        # Verbose should be set (either True or False)
        assert isinstance(agent.verbose, bool)

    print("✓ Agent verbose settings are configured")


def run_all_tests():
    """Run all agent basic tests."""
    print("\n" + "=" * 60)
    print("RUNNING AGENTS BASIC TESTS")
    print("=" * 60 + "\n")

    try:
        test_create_concept_expander_agent()
        test_create_goals_analyzer_agent()
        test_create_framework_selector_agent()
        test_create_phase_designer_agent()
        test_create_teacher_agent()
        test_create_prd_writer_agent()
        test_all_agents_have_backstory()
        test_all_agents_have_goals()
        test_agent_delegation_settings()
        test_agent_verbose_settings()

        print("\n" + "=" * 60)
        print("✓ ALL AGENTS BASIC TESTS PASSED")
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
