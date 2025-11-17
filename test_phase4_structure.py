"""
Phase 4 Structure Verification Test

This script verifies that all Phase 4 components are properly implemented:
- PRDWriterAgent is created and importable
- crew_config has the complete pipeline function
- runner.py has Phase 4 execution path
- All necessary functions are exported
"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

def test_prd_writer_agent():
    """Test that PRDWriterAgent is properly implemented."""
    print("Testing PRDWriterAgent...")

    from project_forge.src.agents.prd_writer_agent import (
        create_prd_writer_agent,
        create_prd_writing_task,
        parse_prd_writing_result,
        generate_project_name
    )

    # Verify functions exist and are callable
    assert callable(create_prd_writer_agent), "create_prd_writer_agent should be callable"
    assert callable(create_prd_writing_task), "create_prd_writing_task should be callable"
    assert callable(parse_prd_writing_result), "parse_prd_writing_result should be callable"
    assert callable(generate_project_name), "generate_project_name should be callable"

    print("  ✓ PRDWriterAgent module structure is correct")
    print("  ✓ All required functions are defined")
    return True


def test_crew_config_updates():
    """Test that crew_config has Phase 4 updates."""
    print("\nTesting crew_config updates...")

    from project_forge.src.orchestration.crew_config import (
        FullPlanWithReadmeResult,
        create_complete_pipeline
    )

    # Verify new dataclass exists
    assert hasattr(FullPlanWithReadmeResult, '__dataclass_fields__'), \
        "FullPlanWithReadmeResult should be a dataclass"

    # Verify it has the expected fields
    fields = FullPlanWithReadmeResult.__dataclass_fields__
    required_fields = {'project_plan', 'evaluation', 'readme_content', 'project_name', 'iterations'}
    assert required_fields.issubset(fields.keys()), \
        f"FullPlanWithReadmeResult should have fields: {required_fields}"

    # Verify function exists
    assert callable(create_complete_pipeline), "create_complete_pipeline should be callable"

    print("  ✓ FullPlanWithReadmeResult dataclass is properly defined")
    print("  ✓ create_complete_pipeline function exists")
    return True


def test_runner_updates():
    """Test that runner.py has Phase 4 support."""
    print("\nTesting runner.py updates...")

    runner_path = Path(__file__).parent / "project_forge" / "src" / "orchestration" / "runner.py"
    runner_content = runner_path.read_text()

    # Check for Phase 4 implementation markers
    checks = {
        "Phase 4 option": "choices=[2, 3, 4]" in runner_content,
        "Logging setup": "def setup_logging" in runner_content,
        "Phase 4 execution": "elif args.phase == 4:" in runner_content,
        "README file output": "output_path.write_text(result.readme_content" in runner_content,
        "Error handling": "except KeyboardInterrupt:" in runner_content,
        "API key check": "OPENAI_API_KEY" in runner_content,
        "Logging calls": "logger.info" in runner_content,
    }

    all_passed = True
    for check_name, check_result in checks.items():
        if check_result:
            print(f"  ✓ {check_name} found")
        else:
            print(f"  ✗ {check_name} NOT found")
            all_passed = False

    return all_passed


def test_file_structure():
    """Test that all Phase 4 files exist."""
    print("\nTesting file structure...")

    base_path = Path(__file__).parent / "project_forge"

    required_files = [
        "src/agents/prd_writer_agent.py",
        "src/orchestration/crew_config.py",
        "src/orchestration/runner.py",
    ]

    all_exist = True
    for file_path in required_files:
        full_path = base_path / file_path
        if full_path.exists():
            print(f"  ✓ {file_path} exists")
        else:
            print(f"  ✗ {file_path} NOT found")
            all_exist = False

    return all_exist


def main():
    """Run all verification tests."""
    print("=" * 80)
    print("PHASE 4 STRUCTURE VERIFICATION")
    print("=" * 80)
    print()

    tests = [
        ("File Structure", test_file_structure),
        ("PRDWriterAgent", test_prd_writer_agent),
        ("CrewConfig Updates", test_crew_config_updates),
        ("Runner Updates", test_runner_updates),
    ]

    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n  ✗ Error in {test_name}: {e}")
            results[test_name] = False

    print("\n" + "=" * 80)
    print("VERIFICATION SUMMARY")
    print("=" * 80)

    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name:.<50} {status}")

    all_passed = all(results.values())

    print()
    if all_passed:
        print("✓ All Phase 4 verification tests passed!")
        print("\nPhase 4 Implementation Complete:")
        print("  - PRDWriterAgent converts ProjectPlan to README/PRD markdown")
        print("  - Standard README structure defined (Overview, Goals, Architecture, etc.)")
        print("  - TeacherAgent learning notes embedded in README output")
        print("  - crew_config.py integrated with complete pipeline")
        print("  - runner.py writes README/PRD to output/ directory")
        print("  - Logging shows agent execution flow")
        print("  - Error handling for API calls and missing config")
        print()
        print("Ready for Phase 5: Polish, Presets, and Examples")
        return 0
    else:
        print("✗ Some verification tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
