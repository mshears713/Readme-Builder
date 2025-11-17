"""
Consistency checking tools for validating project plan integrity.

These tools help EvaluatorAgent ensure that the project plan is internally
consistent - phase counts match expectations, step numbering is correct,
dependencies are valid, etc. Catches structural errors before README generation.

This is a stub implementation for Phase 1. Will be expanded in Phase 3.
"""

from typing import List, Dict, Any
from dataclasses import dataclass, field


@dataclass
class ConsistencyIssue:
    """
    A single consistency problem found in the plan.

    Attributes:
        severity: 'error' (blocks approval) or 'warning' (should fix but not blocking)
        category: Type of issue (e.g., 'phase_count', 'step_numbering', 'dependencies')
        message: Human-readable description of the problem
        location: Where in the plan the issue was found (e.g., 'Phase 2, Step 5')
    """
    severity: str  # 'error' or 'warning'
    category: str
    message: str
    location: str = ""


@dataclass
class ConsistencyReport:
    """
    Results of consistency checking on a project plan.

    Attributes:
        issues: List of all issues found
        passed: Whether the plan passes consistency checks (no errors)
        summary: High-level summary of results
    """
    issues: List[ConsistencyIssue] = field(default_factory=list)
    passed: bool = True
    summary: str = ""

    def has_errors(self) -> bool:
        """Check if any error-level issues were found."""
        return any(issue.severity == 'error' for issue in self.issues)

    def has_warnings(self) -> bool:
        """Check if any warning-level issues were found."""
        return any(issue.severity == 'warning' for issue in self.issues)

    def get_error_count(self) -> int:
        """Count total errors."""
        return sum(1 for issue in self.issues if issue.severity == 'error')

    def get_warning_count(self) -> int:
        """Count total warnings."""
        return sum(1 for issue in self.issues if issue.severity == 'warning')


def check_phase_count(phases: List[Any], expected_count: int = 5) -> ConsistencyReport:
    """
    Verify that the project has the expected number of phases.

    Standard Project Forge plans should have exactly 5 phases. This check
    ensures PhaseDesignerAgent created the right structure.

    Args:
        phases: List of Phase objects from ProjectPlan
        expected_count: Expected number of phases (default: 5)

    Returns:
        ConsistencyReport with any issues found

    Note:
        Stub implementation - will be enhanced in Phase 3 to check
        phase balance, step counts per phase, etc.
    """
    report = ConsistencyReport()

    actual_count = len(phases)
    if actual_count != expected_count:
        report.issues.append(ConsistencyIssue(
            severity='error',
            category='phase_count',
            message=f"Expected {expected_count} phases but found {actual_count}",
            location="ProjectPlan.phases"
        ))
        report.passed = False
    else:
        report.summary = f"Phase count is correct: {expected_count} phases"

    return report


def check_step_numbering(phases: List[Any]) -> ConsistencyReport:
    """
    Verify that steps are numbered sequentially across all phases.

    Steps should have unique, sequential indices starting from 1 and
    continuing across phase boundaries.

    Args:
        phases: List of Phase objects from ProjectPlan

    Returns:
        ConsistencyReport with any issues found

    Note:
        Stub implementation - will be enhanced in Phase 3.
    """
    report = ConsistencyReport()

    # Placeholder logic - to be implemented in Phase 3
    report.summary = "Step numbering check not yet implemented (Phase 3 feature)"

    return report


def check_dependencies(phases: List[Any]) -> ConsistencyReport:
    """
    Verify that step dependencies are valid.

    Checks that:
    - Dependencies reference existing step indices
    - No circular dependencies
    - Dependencies only reference earlier steps

    Args:
        phases: List of Phase objects from ProjectPlan

    Returns:
        ConsistencyReport with any issues found

    Note:
        Stub implementation - will be enhanced in Phase 3.
    """
    report = ConsistencyReport()

    # Placeholder logic - to be implemented in Phase 3
    report.summary = "Dependency check not yet implemented (Phase 3 feature)"

    return report


def validate_project_plan(plan: Any) -> ConsistencyReport:
    """
    Run all consistency checks on a complete project plan.

    This is the main entry point for EvaluatorAgent to validate plan structure.
    Combines all individual checks into a single comprehensive report.

    Args:
        plan: ProjectPlan object to validate

    Returns:
        Combined ConsistencyReport with all issues found

    Note:
        Stub implementation - will be enhanced in Phase 3 to run full suite
        of checks and provide detailed validation.
    """
    report = ConsistencyReport()

    # For Phase 1, just do a basic phase count check
    if hasattr(plan, 'phases'):
        phase_report = check_phase_count(plan.phases)
        report.issues.extend(phase_report.issues)
        report.passed = phase_report.passed and report.passed

    if not report.issues:
        report.summary = "Basic consistency checks passed (Phase 1 validation)"
    else:
        report.summary = f"Found {len(report.issues)} consistency issues"

    return report
