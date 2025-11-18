"""
EvaluatorAgent - Quality control and validation for autonomous AI execution.

This agent evaluates ProjectPlans against quality criteria specifically for
AUTONOMOUS AI EXECUTION. It ensures plans are clear, comprehensive, and
executable by AI agents without user intervention.

Key responsibilities:
- Evaluate plan quality for autonomous executability
- Check for ambiguous language requiring clarification
- Verify implementation guidance is comprehensive and specific
- Run consistency checks (phase counts, step numbering, dependencies)
- Ensure plans enable 1+ hours of continuous AI work
- Decide whether to approve or request refinements
- Provide specific, actionable feedback for improvements

The output is approval/rejection with detailed feedback that can guide
PhaseDesignerAgent or TeacherAgent in refinement iterations.

Teaching Note:
    This agent implements the "evaluation loop" pattern common in multi-agent
    systems. It ensures plans are not just well-structured, but specifically
    executable by AI agents autonomously. We evaluate and iterate until quality
    thresholds are met AND autonomous executability is verified.

    In production systems, you'd typically limit iterations to avoid infinite
    loops and API cost blowout. We use a simple max_iterations approach.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional

from crewai import Agent, Task

from ..models.project_models import ProjectPlan
from ..tools.rubric_tool import (
    RubricScore,
    RubricCriterion,
    evaluate_concept_clarity,
    evaluate_phase_balance,
    evaluate_teaching_clarity,
    evaluate_technical_depth,
    evaluate_feasibility_for_project_type
)
from ..tools.consistency_tool import validate_project_plan, ConsistencyReport


@dataclass
class EvaluationResult:
    """Structured output from heuristic + rubric evaluation."""

    approved: bool
    scores: Dict[RubricCriterion, RubricScore]
    consistency_report: Optional[ConsistencyReport]
    feedback: str
    critical_issues: List[str]
    suggestions: List[str]
    architecture_notes: List[str] = field(default_factory=list)
    resilience_risks: List[str] = field(default_factory=list)
    performance_alerts: List[str] = field(default_factory=list)
    test_recommendations: List[str] = field(default_factory=list)
    naming_feedback: Optional[str] = None


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
        specialist with decades of experience evaluating project plans for
        AUTONOMOUS AI EXECUTION.

        Your expertise includes:
        - Assessing project scope and feasibility for AI agents
        - Evaluating whether plans are clear enough for autonomous execution
        - Identifying ambiguity that would require user clarification
        - Verifying implementation guidance is comprehensive and specific
        - Ensuring plans enable 1+ hours of continuous AI work
        - Providing constructive, actionable feedback
        - Balancing high standards with pragmatism

        Your evaluation philosophy for autonomous execution:
        - Plans must be executable without user intervention
        - Every step must be clear, specific, and unambiguous
        - Implementation guidance must be comprehensive, not minimal
        - No step should require external research or clarification
        - Plans should enable AI agents to work independently for extended periods
        - Better to iterate until autonomously executable than to ship ambiguous plans

        When you evaluate, you:
        - Check for ambiguous language ("if needed", "consider", "optionally")
        - Verify steps have sufficient detail for autonomous implementation
        - Ensure teaching_guidance provides technical details, not just suggestions
        - Look for gaps that would require the AI to stop and ask questions
        - Distinguish between critical problems and minor suggestions
        - Provide specific examples of what needs improvement
        - Consider whether the plan is completable in one continuous session

        You DO NOT:
        - Approve plans with vague or ambiguous steps
        - Accept plans requiring external research or clarification
        - Overlook missing implementation details in teaching_guidance
        - Approve plans that require user input mid-execution
        - Reject plans for arbitrary or subjective reasons
        - Provide vague feedback like "make it better"
        """,
        allow_delegation=False,
        verbose=True
    )


def evaluate_plan_quality(
    plan: ProjectPlan,
    skill_level: str = "intermediate",
    project_type: str = "medium",
    time_constraint: str = "1-2 weeks"
) -> EvaluationResult:
    """
    Evaluate a complete ProjectPlan using heuristic checks.

    This function performs non-LLM evaluation using rubric tools and
    consistency checks. It's faster and more deterministic than LLM-based
    evaluation.

    Enhanced in Phase 5 to:
    - Reject plans that are too big for the time constraint
    - Reject plans that are too trivial for the skill level
    - Use comprehensive rubric evaluations (teaching, technical depth, feasibility)

    Args:
        plan: Complete ProjectPlan with phases, steps, and teaching notes
        skill_level: User's skill level for context
        project_type: Project type ("toy", "medium", "ambitious")
        time_constraint: Time available (e.g., "1 week", "1-2 weeks")

    Returns:
        EvaluationResult with scores, feedback, and approval decision

    Teaching Note:
        Heuristic evaluation is good for structural and quantitative checks.
        Phase 5 enhancement adds sophisticated scope validation to prevent
        users from attempting projects that are too ambitious or too trivial.
    """
    scores: Dict[RubricCriterion, RubricScore] = {}
    critical_issues: List[str] = []
    suggestions: List[str] = []
    architecture_notes: List[str] = []
    resilience_risks: List[str] = []
    performance_alerts: List[str] = []
    test_recommendations: List[str] = []
    naming_feedback: Optional[str] = None

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

    # Phase 5 Enhancement: Evaluate teaching clarity comprehensively
    teaching_score = evaluate_teaching_clarity(plan, skill_level)
    scores[RubricCriterion.TEACHING_VALUE] = teaching_score

    if not teaching_score.passes():
        critical_issues.append(f"Teaching clarity issues: {teaching_score.feedback}")
    elif teaching_score.score < 8:
        suggestions.append(f"Teaching clarity: {teaching_score.feedback}")

    # Phase 5 Enhancement: Evaluate technical depth
    technical_depth_score = evaluate_technical_depth(plan, skill_level)
    scores[RubricCriterion.TECHNICAL_DEPTH] = technical_depth_score

    if not technical_depth_score.passes():
        critical_issues.append(f"Technical depth issues: {technical_depth_score.feedback}")
    elif technical_depth_score.score < 7:
        suggestions.append(f"Technical depth: {technical_depth_score.feedback}")

    # Phase 5 Enhancement: Evaluate feasibility for project type and time constraint
    feasibility_score = evaluate_feasibility_for_project_type(plan, project_type, time_constraint)
    scores[RubricCriterion.FEASIBILITY] = feasibility_score

    if not feasibility_score.passes():
        critical_issues.append(f"SCOPE MISMATCH: {feasibility_score.feedback}")
    elif feasibility_score.score < 7:
        suggestions.append(f"Feasibility concern: {feasibility_score.feedback}")

    # Additional Phase 5 checks for trivial or overambitious plans
    total_steps = sum(len(phase.steps) for phase in plan.phases)
    phase_lengths = [len(phase.steps) for phase in plan.phases if phase.steps]

    if phase_lengths:
        max_len = max(phase_lengths)
        min_len = min(phase_lengths)
        if max_len - min_len > 6:
            architecture_notes.append(
                "Phase sizes vary widely; consider redistributing work for steadier pacing."
            )

    duplicate_phase_names = len({phase.name for phase in plan.phases}) != len(plan.phases)
    if duplicate_phase_names:
        architecture_notes.append("Duplicate phase names detected; rename phases for clarity.")

    # Reject plans that are too trivial
    if total_steps < 20:
        critical_issues.append(
            f"Plan is too trivial: Only {total_steps} steps. Even 'toy' projects should have 20-30 steps to provide meaningful learning."
        )
        performance_alerts.append("Increase the step count to cover a full practice loop.")

    # Reject plans that are clearly overambitious
    if time_constraint.startswith("1 week") or time_constraint == "1 week":
        if total_steps > 40:
            critical_issues.append(
                f"Plan is too ambitious for 1 week: {total_steps} steps. Reduce scope or extend timeline to 1-2 weeks."
            )
            performance_alerts.append("Scope overshoot for 1 week timeline.")
    elif "1-2 week" in time_constraint or "2 week" in time_constraint:
        if total_steps > 60:
            critical_issues.append(
                f"Plan is too ambitious for 2 weeks: {total_steps} steps. Reduce scope or set project_type to 'ambitious' with 3-4 weeks."
            )
            performance_alerts.append("Scope overshoot for 2 week timeline.")

    # Naming/style critique
    phase_titles = [phase.name for phase in plan.phases]
    if phase_titles and not naming_feedback:
        if any(title and title.upper() == title for title in phase_titles):
            naming_feedback = "Phase names use ALL CAPS; prefer sentence or title case for readability."
        elif any(len(title.split()) < 2 for title in phase_titles):
            naming_feedback = "Phase names look too short; add context so the teacher/LLM knows the milestone." 

    # Resilience/test heuristics
    step_texts = [
        (step.title + " " + step.description + " " + (step.teaching_guidance or "")).lower()
        for phase in plan.phases
        for step in phase.steps
    ]

    if step_texts and not any("test" in text for text in step_texts):
        test_recommendations.append("Add a dedicated testing/validation step so the plan closes with verification.")

    if step_texts and not any(keyword in text for text in step_texts for keyword in ["error", "exception", "logging", "retry"]):
        resilience_risks.append("No step mentions error handling or logging; add explicit resilience work.")

    # Check global teaching notes
    if not plan.teaching_notes or len(plan.teaching_notes.strip()) < 50:
        suggestions.append("Global teaching notes are missing or too brief")

    # Phase 5 Enhancement: Check for autonomous executability
    ambiguous_phrases = ["if needed", "consider", "optionally", "you may", "if desired",
                        "feel free to", "think about", "research", "look into"]
    ambiguous_steps = []

    for phase in plan.phases:
        for step in phase.steps:
            # Check step titles and descriptions for ambiguous language
            step_text = (step.title + " " + step.description).lower()
            found_phrases = [phrase for phrase in ambiguous_phrases if phrase in step_text]
            if found_phrases:
                ambiguous_steps.append(f"Step {step.index} contains ambiguous language: {', '.join(found_phrases)}")

            # Check that teaching_guidance is present and substantial
            if not step.teaching_guidance or len(step.teaching_guidance.strip()) < 30:
                critical_issues.append(
                    f"Step {step.index} lacks comprehensive implementation guidance (teaching_guidance too brief or missing)"
                )

    if ambiguous_steps:
        if len(ambiguous_steps) > 5:
            critical_issues.append(
                f"Multiple steps ({len(ambiguous_steps)}) contain ambiguous language that requires clarification. "
                f"For autonomous execution, steps must be decisive and specific."
            )
        else:
            for ambiguous_step in ambiguous_steps:
                suggestions.append(f"Autonomous execution concern: {ambiguous_step}")

    # Overall approval decision
    approved = len(critical_issues) == 0 and all(score.passes() for score in scores.values())

    # Generate feedback summary
    plan_snapshot = (
        f"Architecture snapshot: {len(plan.phases)} phases, {total_steps} steps.\n"
        f"Stack focus → Frontend: {plan.framework.frontend or 'n/a'}, "
        f"Backend: {plan.framework.backend or 'n/a'}, Storage: {plan.framework.storage or 'n/a'}."
    )

    if approved:
        feedback = f"""Plan approved! ✓

{plan_snapshot}

Paragraph 1 — Quality Summary:
Clarity {scores[RubricCriterion.CLARITY].score}/10, Feasibility {scores[RubricCriterion.FEASIBILITY].score}/10,
Teaching Value {scores[RubricCriterion.TEACHING_VALUE].score}/10,
Technical Depth {scores[RubricCriterion.TECHNICAL_DEPTH].score}/10, Balance {scores[RubricCriterion.BALANCE].score}/10.

Paragraph 2 — Structural Notes:
The pacing across phases feels consistent and should keep an AI engaged for 1+ hours. Review the optional notes below
to tighten naming/style and make space for testing before shipping.
"""
        if suggestions:
            feedback += "\nOptional improvements:\n" + "\n".join(f"- {s}" for s in suggestions)
    else:
        feedback = f"""Plan needs revision. ✗

Critical issues to fix:
{chr(10).join(f'- {issue}' for issue in critical_issues)}

Paragraph 1 — Quality Breakdown:
- Clarity: {scores[RubricCriterion.CLARITY].score}/10
- Feasibility: {scores[RubricCriterion.FEASIBILITY].score}/10
- Teaching Value: {scores[RubricCriterion.TEACHING_VALUE].score}/10
- Technical Depth: {scores[RubricCriterion.TECHNICAL_DEPTH].score}/10
- Balance: {scores[RubricCriterion.BALANCE].score}/10

Paragraph 2 — Structural Context:
{plan_snapshot}
"""

    return EvaluationResult(
        approved=approved,
        scores=scores,
        consistency_report=consistency_report,
        feedback=feedback,
        critical_issues=critical_issues,
        suggestions=suggestions,
        architecture_notes=architecture_notes,
        resilience_risks=resilience_risks,
        performance_alerts=performance_alerts,
        test_recommendations=test_recommendations,
        naming_feedback=naming_feedback,
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
            if step.teaching_guidance:
                plan_summary += f"     Educational Guidance: {step.teaching_guidance[:100]}...\n"

    description = f"""
Evaluate this project plan for AUTONOMOUS AI EXECUTION.

CRITICAL: This plan will be executed by an AI agent (like Claude Code) that must complete
all steps in ONE CONTINUOUS SESSION without user intervention. Evaluate whether the plan
enables 1+ hours of autonomous work. Provide multi-paragraph commentary that covers
architecture, naming/style, performance, error-handling, and test coverage recommendations.

{plan_summary}

EVALUATION CRITERIA:

1. CLARITY (0-10):
   - Are steps clear, specific, and unambiguous?
   - Is the progression logical and sequential?
   - Are instructions actionable without clarification?
   - Is there any ambiguous language requiring user input?

2. FEASIBILITY (0-10):
   - Is the scope realistic for autonomous completion in one session?
   - Are step sizes appropriate (30-90 min each) for an AI agent?
   - Are dependencies reasonable and explicit?
   - Can the plan be completed in 1-3 hours of continuous work?

3. AUTONOMOUS EXECUTABILITY (0-10):
   - Does each step have sufficient detail for autonomous implementation?
   - Is teaching_guidance comprehensive with technical specifics?
   - Are there any steps requiring external research or clarification?
   - Can an AI work for 1+ hours without stopping to ask questions?

4. ARCHITECTURE & TESTING NOTES:
   - Comment on naming/style consistency.
   - Flag missing error-handling or testing steps.
   - Suggest resilience or coverage improvements.

4. BALANCE (0-10):
   - Are phases roughly equal in size?
   - Is difficulty well-distributed across phases?
   - Are there clear milestones and deliverables?

OUTPUT FORMAT (JSON):
{{
    "clarity_score": 0-10,
    "clarity_feedback": "Specific observations about clarity for AI execution...",
    "feasibility_score": 0-10,
    "feasibility_feedback": "Specific observations about autonomous completion...",
    "executability_score": 0-10,
    "executability_feedback": "Specific observations about autonomous executability...",
    "balance_score": 0-10,
    "balance_feedback": "Specific observations...",
    "approved": true/false,
    "critical_issues": ["issue1", "issue2"],
    "suggestions": ["suggestion1", "suggestion2"],
    "summary": "Overall evaluation summary for autonomous AI execution..."
}}

Be specific and constructive. Focus on whether an AI can execute this autonomously.
Identify real problems that would block autonomous execution, not nitpicks.
"""

    return Task(
        description=description,
        expected_output="JSON evaluation with scores and feedback",
        agent=agent
    )


def evaluate_project_plan(
    plan: ProjectPlan,
    skill_level: str = "intermediate",
    project_type: str = "medium",
    time_constraint: str = "1-2 weeks",
    use_llm: bool = False
) -> EvaluationResult:
    """
    Main entry point for evaluating a ProjectPlan.

    Combines heuristic and optionally LLM-based evaluation for comprehensive
    quality assessment.

    Phase 5 Enhancement: Now considers project_type and time_constraint to
    reject plans that are too ambitious or too trivial for the user's goals.

    Args:
        plan: Complete ProjectPlan to evaluate
        skill_level: User's skill level
        project_type: Project type ("toy", "medium", "ambitious")
        time_constraint: Time available (e.g., "1 week", "1-2 weeks")
        use_llm: Whether to use LLM-based evaluation (slower but more nuanced)

    Returns:
        EvaluationResult with approval decision and feedback

    Teaching Note:
        The evaluation loop is critical for quality. We start with fast
        heuristic checks, then optionally use LLM for nuanced assessment.
        This two-tier approach balances speed and quality.

        Phase 5 adds sophisticated scope validation to ensure projects are
        "just right" - not too big to finish, not too small to learn from.

    Usage:
        >>> result = evaluate_project_plan(plan, "intermediate", "medium", "1-2 weeks")
        >>> if result.approved:
        >>>     print("Plan approved!")
        >>> else:
        >>>     print(f"Issues: {result.critical_issues}")
    """
    # Always run heuristic evaluation with Phase 5 enhancements
    result = evaluate_plan_quality(plan, skill_level, project_type, time_constraint)

    # Optionally add LLM-based evaluation
    if use_llm and not result.approved:
        # Could implement LLM evaluation here for even more nuanced assessment
        # For Phase 5, the enhanced heuristics are sufficient
        pass

    return result
