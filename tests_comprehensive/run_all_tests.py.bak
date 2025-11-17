"""
Master test runner for Project Forge comprehensive test suite.

This script runs all test modules and provides a summary of results.
It's designed to be run from the command line to verify the entire system.
"""

import sys
import os
from pathlib import Path
import time

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import all test modules
import test_data_models
import test_tools
import test_cli_runner
import test_agents_basic


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_separator():
    """Print a separator line."""
    print("-" * 70)


def run_test_suite(test_module, name):
    """
    Run a test suite and return success status.

    Args:
        test_module: The test module to run
        name: Human-readable name for the test suite

    Returns:
        Tuple of (success: bool, duration: float)
    """
    print(f"\nRunning {name}...")
    print_separator()

    start_time = time.time()

    try:
        success = test_module.run_all_tests()
        duration = time.time() - start_time

        if success:
            print(f"✓ {name} PASSED in {duration:.2f}s")
        else:
            print(f"✗ {name} FAILED in {duration:.2f}s")

        return success, duration

    except Exception as e:
        duration = time.time() - start_time
        print(f"✗ {name} CRASHED in {duration:.2f}s")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False, duration


def main():
    """Run all test suites and report results."""
    print_header("PROJECT FORGE - COMPREHENSIVE TEST SUITE")
    print("\nThis test suite verifies all components of Project Forge")
    print("without making actual API calls to avoid costs.")

    start_time = time.time()

    # Track results
    results = []

    # Define all test suites
    test_suites = [
        (test_data_models, "Data Models Tests"),
        (test_tools, "Tools Tests"),
        (test_cli_runner, "CLI Runner Tests"),
        (test_agents_basic, "Agents Basic Tests"),
    ]

    # Run each test suite
    for test_module, name in test_suites:
        success, duration = run_test_suite(test_module, name)
        results.append({
            'name': name,
            'success': success,
            'duration': duration
        })
        print_separator()

    # Calculate totals
    total_duration = time.time() - start_time
    total_suites = len(results)
    passed_suites = sum(1 for r in results if r['success'])
    failed_suites = total_suites - passed_suites

    # Print summary
    print_header("TEST SUMMARY")

    print(f"\nTotal Test Suites: {total_suites}")
    print(f"Passed: {passed_suites}")
    print(f"Failed: {failed_suites}")
    print(f"Total Duration: {total_duration:.2f}s")

    print("\nDetailed Results:")
    print_separator()

    for result in results:
        status = "✓ PASS" if result['success'] else "✗ FAIL"
        print(f"{status:8} | {result['duration']:6.2f}s | {result['name']}")

    print_separator()

    # Overall result
    if failed_suites == 0:
        print("\n🎉 ALL TESTS PASSED!")
        print("\nProject Forge is ready to run. The core components are working correctly.")
        print("\nNote: These tests verify structure and logic without making API calls.")
        print("To test the full pipeline, you'll need to run the actual CLI with a valid API key.")
        return_code = 0
    else:
        print(f"\n⚠️  {failed_suites} TEST SUITE(S) FAILED")
        print("\nPlease review the failed tests above and fix any issues.")
        print("The program may not run correctly until all tests pass.")
        return_code = 1

    print_header("END OF TEST SUITE")

    return return_code


if __name__ == "__main__":
    return_code = main()
    sys.exit(return_code)
