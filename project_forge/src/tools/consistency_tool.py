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

    Teaching Note (Phase 3):
        Sequential numbering across phases helps users track overall progress
        through the project. Each step should have a unique global index.
    """
    report = ConsistencyReport()

    if not phases:
        report.summary = "No phases to check"
        return report

    expected_index = 1
    all_indices = []

    for phase in phases:
        for step in phase.steps:
            all_indices.append(step.index)

            if step.index != expected_index:
                report.issues.append(ConsistencyIssue(
                    severity='warning',
                    category='step_numbering',
                    message=f"Expected step index {expected_index} but found {step.index}",
                    location=f"Phase {phase.index}, Step '{step.title}'"
                ))

            expected_index += 1

    # Check for duplicate indices
    duplicates = [idx for idx in set(all_indices) if all_indices.count(idx) > 1]
    if duplicates:
        for dup in duplicates:
            report.issues.append(ConsistencyIssue(
                severity='error',
                category='step_numbering',
                message=f"Duplicate step index: {dup}",
                location="Multiple steps"
            ))
        report.passed = False

    if not report.issues:
        total_steps = len(all_indices)
        report.summary = f"Step numbering is correct: {total_steps} sequential steps"

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

    Teaching Note (Phase 3):
        Valid dependencies ensure that the build plan is executable in order.
        Steps should only depend on earlier steps to avoid circular logic.
    """
    report = ConsistencyReport()

    if not phases:
        report.summary = "No phases to check"
        return report

    # Collect all valid step indices
    all_step_indices = []
    for phase in phases:
        for step in phase.steps:
            all_step_indices.append(step.index)

    # Check each step's dependencies
    for phase in phases:
        for step in phase.steps:
            for dep_index in step.dependencies:
                # Check if dependency exists
                if dep_index not in all_step_indices:
                    report.issues.append(ConsistencyIssue(
                        severity='error',
                        category='dependencies',
                        message=f"References non-existent step {dep_index}",
                        location=f"Phase {phase.index}, Step {step.index} '{step.title}'"
                    ))
                    report.passed = False

                # Check if dependency is earlier (no forward or self-references)
                elif dep_index >= step.index:
                    report.issues.append(ConsistencyIssue(
                        severity='error',
                        category='dependencies',
                        message=f"References step {dep_index} which is not earlier than current step {step.index}",
                        location=f"Phase {phase.index}, Step {step.index} '{step.title}'"
                    ))
                    report.passed = False

    if not report.issues:
        report.summary = "All dependencies are valid"

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

    Teaching Note (Phase 3):
        Comprehensive validation catches structural problems before README
        generation. This prevents generating broken plans that users can't execute.
    """
    report = ConsistencyReport()

    if not hasattr(plan, 'phases'):
        report.issues.append(ConsistencyIssue(
            severity='error',
            category='structure',
            message="ProjectPlan has no 'phases' attribute",
            location="ProjectPlan"
        ))
        report.passed = False
        report.summary = "Critical structure error"
        return report

    # Run all consistency checks
    phase_count_report = check_phase_count(plan.phases)
    report.issues.extend(phase_count_report.issues)
    if not phase_count_report.passed:
        report.passed = False

    step_numbering_report = check_step_numbering(plan.phases)
    report.issues.extend(step_numbering_report.issues)
    if not step_numbering_report.passed:
        report.passed = False

    dependencies_report = check_dependencies(plan.phases)
    report.issues.extend(dependencies_report.issues)
    if not dependencies_report.passed:
        report.passed = False

    # Generate summary
    if not report.issues:
        total_steps = sum(len(phase.steps) for phase in plan.phases)
        report.summary = f"All consistency checks passed: {len(plan.phases)} phases, {total_steps} steps"
    else:
        error_count = report.get_error_count()
        warning_count = report.get_warning_count()
        report.summary = f"Found {error_count} errors and {warning_count} warnings"

    return report
