"""
EvaluatorAgent - Quality control and validation for project plans.

This agent evaluates ProjectPlans against quality criteria (clarity, feasibility,
teaching value, balance) and decides whether to approve or request revisions.
It acts as a quality gate before final README generation.

Key responsibilities:
- Evaluate plan quality using rubrics (clarity, feasibility, teaching value, balance)
- Run consistency checks (phase counts, step numbering, dependencies)
- Decide whether to approve or request refinements
- Provide specific, actionable feedback for improvements
- Support multiple evaluation modes (concept, goals, full plan)

The output is approval/rejection with detailed feedback that can guide
PhaseDesignerAgent or TeacherAgent in refinement iterations.

Teaching Note:
    This agent implements the "evaluation loop" pattern common in multi-agent
    systems. Rather than blindly accepting the first output, we evaluate and
    iterate until quality thresholds are met. This dramatically improves the
    quality of generated plans.

    In production systems, you'd typically limit iterations to avoid infinite
    loops and API cost blowout. We use a simple max_iterations approach.
"""

from crewai import Agent, Task
from typing import List, Dict, Any, Optional
import json
from dataclasses import dataclass

from ..models.project_models import ProjectIdea, ProjectGoals, ProjectPlan
from ..tools.rubric_tool import (
    RubricScore,
    RubricCriterion,
    evaluate_concept_clarity,
    evaluate_phase_balance
)
from ..tools.consistency_tool import validate_project_plan, ConsistencyReport


@dataclass
class EvaluationResult:
    """
    Result of evaluating a project component.

    Attributes:
        approved: Whether the component passes evaluation
        scores: Dict of rubric scores by criterion
        consistency_report: Structural consistency check results
        feedback: Detailed feedback and suggestions
        critical_issues: List of blocking problems that must be fixed
        suggestions: List of optional improvements
    """
    approved: bool
    scores: Dict[RubricCriterion, RubricScore]
    consistency_report: Optional[ConsistencyReport]
    feedback: str
    critical_issues: List[str]
    suggestions: List[str]


def create_evaluator_agent() -> Agent:
    """
    Create the EvaluatorAgent with specialized focus on quality assessment.

    This agent has high standards and provides constructive feedback. It
    understands what makes a good project plan and can articulate specific
    improvements.

    Returns:
        CrewAI Agent configured for evaluation

    Teaching Note:
        The backstory shapes this agent to be thorough but constructive.
        We want it to catch real problems but not be needlessly picky about
        subjective preferences.
    """
    return Agent(
        role="Project Plan Evaluator and Quality Assurance",
        goal="Ensure project plans meet quality standards for clarity, feasibility, teaching value, and structural integrity",
        backstory="""You are an expert technical reviewer and quality assurance
        specialist with decades of experience evaluating project plans and
        educational materials.

        Your expertise includes:
        - Assessing project scope and feasibility
        - Evaluating learning design and pedagogical quality
        - Identifying structural problems and inconsistencies
        - Providing constructive, actionable feedback
        - Balancing high standards with pragmatism

        Your evaluation philosophy:
        - Quality matters more than speed
        - Specific feedback is more valuable than general criticism
        - Plans should be realistic and achievable
        - Learning value should be explicit and clear
        - Structure should be consistent and logical
        - Better to iterate than to ship subpar work

        When you evaluate, you:
        - Look for concrete, actionable issues
        - Distinguish between critical problems and minor suggestions
        - Provide specific examples of what needs improvement
        - Consider the user's skill level and constraints
        - Focus on whether the plan will actually work in practice

        You DO NOT:
        - Reject plans for arbitrary or subjective reasons
        - Request changes without clear justification
        - Focus on superficial issues while missing structural problems
        - Provide vague feedback like "make it better"
        - Approve clearly broken or unrealistic plans""",
        allow_delegation=False,
        verbose=True
    )


def evaluate_plan_quality(
    plan: ProjectPlan,
    skill_level: str = "intermediate"
) -> EvaluationResult:
    """
    Evaluate a complete ProjectPlan using heuristic checks.

    This function performs non-LLM evaluation using rubric tools and
    consistency checks. It's faster and more deterministic than LLM-based
    evaluation.

    Args:
        plan: Complete ProjectPlan with phases, steps, and teaching notes
        skill_level: User's skill level for context

    Returns:
        EvaluationResult with scores, feedback, and approval decision

    Teaching Note:
        Heuristic evaluation is good for structural and quantitative checks.
        For more nuanced quality assessment (like evaluating teaching quality),
        you'd use an LLM-based evaluation task. We keep it simple here for
        Phase 3 but could enhance in Phase 5.
    """
    scores = {}
    critical_issues = []
    suggestions = []

    # Run consistency checks
    consistency_report = validate_project_plan(plan)

    if consistency_report.has_errors():
        critical_issues.append(
            f"Structural errors: {consistency_report.summary}"
        )
        for issue in consistency_report.issues:
            if issue.severity == 'error':
                critical_issues.append(f"{issue.category}: {issue.message} ({issue.location})")

    if consistency_report.has_warnings():
        for issue in consistency_report.issues:
            if issue.severity == 'warning':
                suggestions.append(f"{issue.category}: {issue.message} ({issue.location})")

    # Evaluate concept clarity
    clarity_score = evaluate_concept_clarity(plan.idea.refined_summary)
    scores[RubricCriterion.CLARITY] = clarity_score

    if not clarity_score.passes():
        critical_issues.append(f"Clarity issues: {clarity_score.feedback}")

    # Evaluate phase balance
    balance_score = evaluate_phase_balance(plan.phases)
    scores[RubricCriterion.BALANCE] = balance_score

    if not balance_score.passes():
        critical_issues.append(f"Balance issues: {balance_score.feedback}")
    elif balance_score.score < 8:
        suggestions.append(f"Balance could be improved: {balance_score.feedback}")

    # Check teaching enrichment
    steps_with_teaching = sum(
        1 for phase in plan.phases
        for step in phase.steps
        if step.what_you_learn and len(step.what_you_learn.strip()) > 10
    )
    total_steps = sum(len(phase.steps) for phase in plan.phases)

    if steps_with_teaching < total_steps * 0.8:  # At least 80% of steps should have teaching notes
        critical_issues.append(
            f"Teaching enrichment incomplete: only {steps_with_teaching}/{total_steps} steps have learning annotations"
        )

    # Check global teaching notes
    if not plan.teaching_notes or len(plan.teaching_notes.strip()) < 50:
        suggestions.append("Global teaching notes are missing or too brief")

    # Overall approval decision
    approved = len(critical_issues) == 0 and all(score.passes() for score in scores.values())

    # Generate feedback summary
    if approved:
        feedback = f"""Plan approved!

Scores:
- Clarity: {scores[RubricCriterion.CLARITY].score}/10
- Balance: {scores[RubricCriterion.BALANCE].score}/10

Structure: {total_steps} steps across {len(plan.phases)} phases
Teaching: {steps_with_teaching}/{total_steps} steps have learning annotations
"""
        if suggestions:
            feedback += "\nOptional improvements:\n" + "\n".join(f"- {s}" for s in suggestions)
    else:
        feedback = f"""Plan needs revision.

Critical issues to fix:
{chr(10).join(f'- {issue}' for issue in critical_issues)}

Current scores:
- Clarity: {scores[RubricCriterion.CLARITY].score}/10
- Balance: {scores[RubricCriterion.BALANCE].score}/10
"""

    return EvaluationResult(
        approved=approved,
        scores=scores,
        consistency_report=consistency_report,
        feedback=feedback,
        critical_issues=critical_issues,
        suggestions=suggestions
    )


def create_plan_evaluation_task(
    agent: Agent,
    plan: ProjectPlan,
    skill_level: str = "intermediate"
) -> Task:
    """
    Create an LLM-based evaluation task for nuanced quality assessment.

    This task asks the LLM to evaluate subjective aspects like teaching
    quality, step clarity, and overall plan coherence that are hard to
    assess with heuristics alone.

    Args:
        agent: The EvaluatorAgent
        plan: Complete ProjectPlan to evaluate
        skill_level: User's skill level

    Returns:
        CrewAI Task configured for plan evaluation

    Teaching Note:
        LLM-based evaluation is more expensive but can catch subtle issues
        that heuristics miss. Use it sparingly and combine with heuristic
        checks for best results.

        This is an advanced feature that could be implemented in Phase 5.
        For Phase 3, we rely primarily on the heuristic evaluation above.
    """
    # Build a summary of the plan
    plan_summary = f"""
PROJECT: {plan.idea.refined_summary}

LEARNING GOALS: {', '.join(plan.goals.learning_goals)}
TECHNICAL GOALS: {', '.join(plan.goals.technical_goals)}

STRUCTURE: {len(plan.phases)} phases, {sum(len(p.steps) for p in plan.phases)} total steps

SAMPLE STEPS:
"""
    # Show first few steps as examples
    for phase in plan.phases[:2]:
        plan_summary += f"\nPhase {phase.index}: {phase.name}\n"
        for step in phase.steps[:3]:
            plan_summary += f"  {step.index}. {step.title}\n"
            if step.what_you_learn:
                plan_summary += f"     Learn: {step.what_you_learn[:100]}...\n"

    description = f"""
Evaluate this project plan for quality and learning value.

{plan_summary}

EVALUATION CRITERIA:

1. CLARITY (0-10):
   - Are steps clear and specific?
   - Is the progression logical?
   - Are instructions actionable?

2. FEASIBILITY (0-10):
   - Is the scope realistic for {skill_level} users?
   - Are step sizes appropriate (30-90 min each)?
   - Are dependencies reasonable?

3. TEACHING VALUE (0-10):
   - Are learning objectives clear?
   - Do teaching annotations add value?
   - Is the learning arc progressive?

4. BALANCE (0-10):
   - Are phases roughly equal in size?
   - Is difficulty well-distributed?
   - Are there clear milestones?

OUTPUT FORMAT (JSON):
{{
    "clarity_score": 0-10,
    "clarity_feedback": "Specific observations...",
    "feasibility_score": 0-10,
    "feasibility_feedback": "Specific observations...",
    "teaching_score": 0-10,
    "teaching_feedback": "Specific observations...",
    "balance_score": 0-10,
    "balance_feedback": "Specific observations...",
    "approved": true/false,
    "critical_issues": ["issue1", "issue2"],
    "suggestions": ["suggestion1", "suggestion2"],
    "summary": "Overall evaluation summary..."
}}

Be specific and constructive. Identify real problems, not nitpicks.
"""

    return Task(
        description=description,
        expected_output="JSON evaluation with scores and feedback",
        agent=agent
    )


def evaluate_project_plan(
    plan: ProjectPlan,
    skill_level: str = "intermediate",
    use_llm: bool = False
) -> EvaluationResult:
    """
    Main entry point for evaluating a ProjectPlan.

    Combines heuristic and optionally LLM-based evaluation for comprehensive
    quality assessment.

    Args:
        plan: Complete ProjectPlan to evaluate
        skill_level: User's skill level
        use_llm: Whether to use LLM-based evaluation (slower but more nuanced)

    Returns:
        EvaluationResult with approval decision and feedback

    Teaching Note:
        The evaluation loop is critical for quality. We start with fast
        heuristic checks, then optionally use LLM for nuanced assessment.
        This two-tier approach balances speed and quality.

    Usage:
        >>> result = evaluate_project_plan(plan, "intermediate")
        >>> if result.approved:
        >>>     print("Plan approved!")
        >>> else:
        >>>     print(f"Issues: {result.critical_issues}")
    """
    # Always run heuristic evaluation
    result = evaluate_plan_quality(plan, skill_level)

    # Optionally add LLM-based evaluation
    if use_llm and not result.approved:
        # Could implement LLM evaluation here in Phase 5
        # For Phase 3, we rely on heuristics only
        pass

    return result
