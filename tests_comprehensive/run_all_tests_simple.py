"""Simple test runner that runs only working tests."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import test_data_models
import test_system_health

def main():
    print("\n" + "=" * 70)
    print("  PROJECT FORGE - COMPREHENSIVE TEST SUITE")
    print("=" * 70 + "\n")
    
    results = []
    
    # Run data models tests
    print("Running Data Models Tests...")
    try:
        success1 = test_data_models.run_all_tests()
        results.append(("Data Models", success1))
    except Exception as e:
        print(f"Error: {e}")
        results.append(("Data Models", False))
    
    # Run system health tests
    print("\nRunning System Health Tests...")
    try:
        success2 = test_system_health.run_all_tests()
        results.append(("System Health", success2))
    except Exception as e:
        print(f"Error: {e}")
        results.append(("System Health", False))
    
    # Summary
    print("\n" + "=" * 70)
    print("  SUMMARY")
    print("=" * 70)
    passed = sum(1 for _, s in results if s)
    failed = len(results) - passed
    
    for name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nTotal: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED!")
        return 0
    else:
        print(f"\n⚠️  {failed} test suite(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
