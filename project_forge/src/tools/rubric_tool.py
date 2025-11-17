"""
Evaluation rubric tools for assessing project plans and outputs.

EvaluatorAgent uses these rubrics to score different aspects of the project plan
(clarity, feasibility, teaching value) and decide whether to approve or request
revisions. Provides structured scoring with explanations.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from enum import Enum


class RubricCriterion(Enum):
    """Evaluation criteria for project plans."""
    CLARITY = "clarity"
    FEASIBILITY = "feasibility"
    TEACHING_VALUE = "teaching_value"
    TECHNICAL_DEPTH = "technical_depth"
    COMPLETENESS = "completeness"
    BALANCE = "balance"


@dataclass
class RubricScore:
    """
    Score for a single evaluation criterion.

    Attributes:
        criterion: Which aspect is being evaluated
        score: Numeric score (0-10, where 10 is best)
        feedback: Explanation of the score and suggestions for improvement
        pass_threshold: Minimum score needed to pass this criterion
    """
    criterion: RubricCriterion
    score: int
    feedback: str = ""
    pass_threshold: int = 7

    def passes(self) -> bool:
        """Check if this score meets the passing threshold."""
        return self.score >= self.pass_threshold


@dataclass
class RubricEvaluation:
    """
    Complete evaluation of a project component.

    Attributes:
        component: What is being evaluated (e.g., "concept", "plan", "phase_design")
        scores: List of scores for different criteria
        overall_pass: Whether the evaluation passes overall
        summary: High-level summary of the evaluation
        recommendations: List of specific improvements to make
    """
    component: str
    scores: List[RubricScore] = field(default_factory=list)
    overall_pass: bool = False
    summary: str = ""
    recommendations: List[str] = field(default_factory=list)

    def calculate_overall_pass(self) -> bool:
        """Determine if all criteria pass their thresholds."""
        if not self.scores:
            return False
        return all(score.passes() for score in self.scores)

    def get_average_score(self) -> float:
        """Calculate average score across all criteria."""
        if not self.scores:
            return 0.0
        return sum(score.score for score in self.scores) / len(self.scores)


def create_clarity_rubric() -> Dict[str, Any]:
    """
    Define the clarity evaluation rubric.

    Clarity measures how well the project concept or plan is explained:
    - Clear objectives and scope
    - Unambiguous language
    - Logical organization

    Returns:
        Dict with rubric criteria and scoring guidelines
    """
    return {
        "name": "Clarity",
        "description": "How clearly is the project concept/plan explained?",
        "score_levels": {
            10: "Crystal clear, no ambiguity, anyone could understand it",
            8: "Very clear with minor room for interpretation",
            6: "Mostly clear but some vague sections",
            4: "Several unclear or confusing parts",
            2: "Difficult to understand overall intent",
            0: "Completely unclear or incoherent"
        },
        "pass_threshold": 7
    }


def create_feasibility_rubric() -> Dict[str, Any]:
    """
    Define the feasibility evaluation rubric.

    Feasibility measures whether the project is realistic given constraints:
    - Appropriate scope for time/skill level
    - Not too ambitious or trivial
    - Reasonable technical complexity

    Returns:
        Dict with rubric criteria and scoring guidelines
    """
    return {
        "name": "Feasibility",
        "description": "Is this project realistic to complete?",
        "score_levels": {
            10: "Perfectly scoped, realistic timeline, appropriate complexity",
            8: "Feasible with minor concerns about scope or time",
            6: "Doable but might be tight on time or complexity",
            4: "Questionable - may be too ambitious or too simple",
            2: "Likely infeasible - scope or complexity mismatch",
            0: "Completely unrealistic or trivial"
        },
        "pass_threshold": 6
    }


def create_teaching_value_rubric() -> Dict[str, Any]:
    """
    Define the teaching value evaluation rubric.

    Teaching value measures how much the user will learn:
    - Clear learning objectives
    - Progressive skill building
    - Good explanations of concepts
    - Appropriate challenge level

    Returns:
        Dict with rubric criteria and scoring guidelines
    """
    return {
        "name": "Teaching Value",
        "description": "How much will the user learn from this project?",
        "score_levels": {
            10: "Excellent learning arc, clear teaching, perfect difficulty",
            8: "Strong learning value with good explanations",
            6: "Decent learning but could be more pedagogical",
            4: "Some learning but weak teaching structure",
            2: "Minimal learning value or poor teaching approach",
            0: "No clear learning objectives or value"
        },
        "pass_threshold": 7
    }


def create_completeness_rubric() -> Dict[str, Any]:
    """
    Define the completeness evaluation rubric.

    Completeness measures whether all required components are present:
    - All phases and steps defined
    - Framework selections made
    - Goals articulated
    - No missing critical information

    Returns:
        Dict with rubric criteria and scoring guidelines
    """
    return {
        "name": "Completeness",
        "description": "Are all required components present?",
        "score_levels": {
            10: "Everything present, fully detailed, no gaps",
            8: "All major components present, minor details missing",
            6: "Most components present but some gaps",
            4: "Several missing components or major gaps",
            2: "Many critical components missing",
            0: "Severely incomplete"
        },
        "pass_threshold": 8
    }


def create_balance_rubric() -> Dict[str, Any]:
    """
    Define the balance evaluation rubric.

    Balance measures even distribution of work and appropriate pacing:
    - Phases are roughly equal in size
    - No phase is empty or overloaded
    - Logical progression of difficulty
    - Steps build on each other

    Returns:
        Dict with rubric criteria and scoring guidelines
    """
    return {
        "name": "Balance",
        "description": "Is the work evenly distributed and well-paced?",
        "score_levels": {
            10: "Perfect balance, smooth progression, logical dependencies",
            8: "Well balanced with minor unevenness",
            6: "Acceptable balance but some phases heavy/light",
            4: "Noticeable imbalance in phase sizes or difficulty",
            2: "Severe imbalance - some phases empty or overloaded",
            0: "Completely unbalanced or illogical structure"
        },
        "pass_threshold": 6
    }


def create_technical_depth_rubric() -> Dict[str, Any]:
    """
    Define the technical depth evaluation rubric.

    Technical depth measures the sophistication and learning potential of the
    technical implementation:
    - Appropriate use of advanced concepts for skill level
    - Real-world patterns and best practices
    - Exposure to production-quality techniques
    - Balance between learning and practical application

    Returns:
        Dict with rubric criteria and scoring guidelines

    Teaching Note:
        Technical depth is different from teaching value. A project can have
        great teaching (clear explanations) but low technical depth (trivial
        implementation). We want both: challenging technical concepts explained
        clearly.
    """
    return {
        "name": "Technical Depth",
        "description": "Does the project teach meaningful technical concepts?",
        "score_levels": {
            10: "Rich technical learning with advanced concepts, best practices, real-world patterns",
            8: "Strong technical content with good depth and practical skills",
            6: "Moderate technical depth, covers important concepts but not deeply",
            4: "Shallow technical depth, basic concepts only",
            2: "Minimal technical learning, mostly trivial implementations",
            0: "No meaningful technical depth or learning"
        },
        "pass_threshold": 6
    }


def get_all_rubrics() -> Dict[RubricCriterion, Dict[str, Any]]:
    """
    Get all available evaluation rubrics.

    Returns:
        Dict mapping criterion enum to rubric definition
    """
    return {
        RubricCriterion.CLARITY: create_clarity_rubric(),
        RubricCriterion.FEASIBILITY: create_feasibility_rubric(),
        RubricCriterion.TEACHING_VALUE: create_teaching_value_rubric(),
        RubricCriterion.TECHNICAL_DEPTH: create_technical_depth_rubric(),
        RubricCriterion.COMPLETENESS: create_completeness_rubric(),
        RubricCriterion.BALANCE: create_balance_rubric(),
    }


def evaluate_concept_clarity(concept_text: str) -> RubricScore:
    """
    Quick evaluation of concept clarity (used in Phase 2).

    Checks basic clarity metrics:
    - Length is reasonable (not too short/long)
    - Contains concrete keywords
    - Not overly vague

    Args:
        concept_text: The refined project concept to evaluate

    Returns:
        RubricScore for clarity

    Note:
        This is a simple heuristic version. In later phases, EvaluatorAgent
        will use LLM-based evaluation for more nuanced assessment.
    """
    score = 10  # Start optimistic
    feedback_points = []

    # Check length
    word_count = len(concept_text.split())
    if word_count < 10:
        score -= 3
        feedback_points.append("Concept is too brief - needs more detail")
    elif word_count > 200:
        score -= 2
        feedback_points.append("Concept is quite verbose - could be more concise")

    # Check for vague words
    vague_words = ['something', 'stuff', 'things', 'maybe', 'somehow']
    vague_count = sum(1 for word in vague_words if word in concept_text.lower())
    if vague_count > 2:
        score -= 2
        feedback_points.append(f"Contains {vague_count} vague terms - be more specific")

    # Check for technical specificity (presence of technical terms)
    if not any(char.isupper() for char in concept_text):  # No proper nouns/acronyms
        score -= 1
        feedback_points.append("Could mention specific technologies or frameworks")

    feedback = " | ".join(feedback_points) if feedback_points else "Concept is clear and well-articulated"

    return RubricScore(
        criterion=RubricCriterion.CLARITY,
        score=max(0, score),
        feedback=feedback,
        pass_threshold=7
    )


def evaluate_phase_balance(phases: List[Any]) -> RubricScore:
    """
    Evaluate whether phases are well-balanced in terms of steps and work distribution.

    Phase 3 enhancement: checks that phases have appropriate number of steps
    and aren't too empty or overloaded.

    Args:
        phases: List of Phase objects from ProjectPlan

    Returns:
        RubricScore for balance

    Teaching Note:
        Balance is important for maintaining momentum. Phases that are too
        small feel trivial, while phases that are too large feel overwhelming.
        We aim for roughly 8-12 steps per phase for good pacing.
    """
    score = 10
    feedback_points = []

    if not phases:
        return RubricScore(
            criterion=RubricCriterion.BALANCE,
            score=0,
            feedback="No phases to evaluate",
            pass_threshold=6
        )

    # Check total phase count
    if len(phases) != 5:
        score -= 3
        feedback_points.append(f"Expected 5 phases but found {len(phases)}")

    # Check step distribution
    step_counts = [len(phase.steps) for phase in phases]
    total_steps = sum(step_counts)
    avg_steps = total_steps / len(phases) if phases else 0

    # Check for empty or nearly empty phases
    empty_phases = [i + 1 for i, count in enumerate(step_counts) if count < 3]
    if empty_phases:
        score -= 2
        feedback_points.append(f"Phases {empty_phases} have too few steps (< 3)")

    # Check for overloaded phases
    overloaded_phases = [i + 1 for i, count in enumerate(step_counts) if count > 15]
    if overloaded_phases:
        score -= 2
        feedback_points.append(f"Phases {overloaded_phases} are overloaded (> 15 steps)")

    # Check variance (phases should be roughly similar in size)
    if step_counts:
        variance = sum((count - avg_steps) ** 2 for count in step_counts) / len(step_counts)
        if variance > 16:  # Standard deviation > 4
            score -= 1
            feedback_points.append(f"Uneven step distribution (counts: {step_counts})")

    # Check total step count
    if total_steps < 40:
        score -= 1
        feedback_points.append(f"Only {total_steps} total steps - plan may be underscoped")
    elif total_steps > 60:
        score -= 1
        feedback_points.append(f"{total_steps} total steps - plan may be overscoped")

    feedback = " | ".join(feedback_points) if feedback_points else f"Well-balanced: {len(phases)} phases with {total_steps} steps (avg {avg_steps:.1f} per phase)"

    return RubricScore(
        criterion=RubricCriterion.BALANCE,
        score=max(0, score),
        feedback=feedback,
        pass_threshold=6
    )


def evaluate_teaching_clarity(plan: Any, skill_level: str = "intermediate") -> RubricScore:
    """
    Evaluate the teaching clarity of a project plan.

    This assesses how well the plan explains concepts and supports learning:
    - Presence of "what you'll learn" annotations
    - Quality and detail of teaching notes
    - Appropriate depth for skill level
    - Progressive complexity throughout phases

    Args:
        plan: ProjectPlan object to evaluate
        skill_level: User's skill level (affects expectations)

    Returns:
        RubricScore for teaching clarity

    Teaching Note:
        Good teaching clarity means a beginner can follow along without getting
        lost, while still being challenged. Steps should explain WHY, not just WHAT.
    """
    score = 10
    feedback_points = []

    # Check for educational guidance in steps
    total_steps = sum(len(phase.steps) for phase in plan.phases)
    steps_with_guidance = sum(
        1 for phase in plan.phases for step in phase.steps
        if hasattr(step, 'teaching_guidance') and step.teaching_guidance and len(step.teaching_guidance.strip()) > 20
    )

    guidance_coverage = (steps_with_guidance / total_steps * 100) if total_steps > 0 else 0

    if guidance_coverage < 50:
        score -= 3
        feedback_points.append(f"Only {guidance_coverage:.0f}% of steps have educational guidance - aim for 80%+")
    elif guidance_coverage < 80:
        score -= 1
        feedback_points.append(f"{guidance_coverage:.0f}% of steps have educational guidance - good but could be higher")

    # Check global teaching notes
    teaching_notes_length = len(plan.teaching_notes) if hasattr(plan, 'teaching_notes') else 0
    if teaching_notes_length < 200:
        score -= 2
        feedback_points.append("Global teaching notes are too brief - should provide pedagogical arc overview")
    elif teaching_notes_length < 500:
        score -= 1
        feedback_points.append("Global teaching notes could be more detailed")

    # Check for progressive complexity (later phases should introduce more advanced concepts)
    # Simple heuristic: later phase names should indicate progression
    advanced_keywords = ['advanced', 'production', 'deployment', 'optimization', 'polish', 'testing']
    basic_keywords = ['setup', 'foundation', 'basics', 'introduction', 'getting started']

    early_phases = plan.phases[:2] if len(plan.phases) >= 2 else []
    late_phases = plan.phases[-2:] if len(plan.phases) >= 2 else []

    early_has_basics = any(
        any(keyword in phase.name.lower() for keyword in basic_keywords)
        for phase in early_phases
    )
    late_has_advanced = any(
        any(keyword in phase.name.lower() for keyword in advanced_keywords)
        for phase in late_phases
    )

    if not early_has_basics:
        score -= 1
        feedback_points.append("Early phases should emphasize foundations and basics")

    if not late_has_advanced and skill_level != "beginner":
        score -= 1
        feedback_points.append("Later phases should introduce more advanced concepts")

    # Skill level adjustments
    if skill_level == "beginner" and learning_coverage < 90:
        score -= 1
        feedback_points.append("Beginner projects need very thorough teaching annotations (aim for 90%+)")

    feedback = " | ".join(feedback_points) if feedback_points else f"Excellent teaching clarity with {learning_coverage:.0f}% learning coverage"

    return RubricScore(
        criterion=RubricCriterion.TEACHING_VALUE,
        score=max(0, score),
        feedback=feedback,
        pass_threshold=7
    )


def evaluate_technical_depth(plan: Any, skill_level: str = "intermediate") -> RubricScore:
    """
    Evaluate the technical depth and sophistication of a project plan.

    Assesses whether the project teaches meaningful technical concepts:
    - Use of appropriate frameworks and tools
    - Exposure to real-world patterns (testing, deployment, error handling)
    - Balance of breadth and depth
    - Appropriate challenge for skill level

    Args:
        plan: ProjectPlan object to evaluate
        skill_level: User's skill level (affects depth expectations)

    Returns:
        RubricScore for technical depth

    Teaching Note:
        Technical depth should match skill level. Beginners need foundational
        concepts thoroughly explained. Advanced users need production patterns
        and sophisticated architectures.
    """
    score = 10
    feedback_points = []

    # Check for presence of advanced topics across all steps
    all_step_titles = [
        step.title.lower()
        for phase in plan.phases
        for step in phase.steps
    ]
    all_step_descriptions = [
        step.description.lower()
        for phase in plan.phases
        for step in phase.steps
    ]

    # Technical depth indicators
    testing_keywords = ['test', 'testing', 'pytest', 'unittest', 'tdd']
    deployment_keywords = ['deploy', 'deployment', 'production', 'docker', 'ci/cd']
    architecture_keywords = ['architecture', 'design pattern', 'solid', 'refactor', 'modular']
    error_handling_keywords = ['error', 'exception', 'logging', 'validation', 'edge case']
    database_keywords = ['database', 'migration', 'query', 'index', 'transaction']
    security_keywords = ['security', 'authentication', 'authorization', 'encryption', 'sanitize']

    all_text = ' '.join(all_step_titles + all_step_descriptions)

    has_testing = any(keyword in all_text for keyword in testing_keywords)
    has_deployment = any(keyword in all_text for keyword in deployment_keywords)
    has_architecture = any(keyword in all_text for keyword in architecture_keywords)
    has_error_handling = any(keyword in all_text for keyword in error_handling_keywords)
    has_database = any(keyword in all_text for keyword in database_keywords)
    has_security = any(keyword in all_text for keyword in security_keywords)

    depth_indicators = [
        has_testing, has_deployment, has_architecture,
        has_error_handling, has_database, has_security
    ]
    depth_score = sum(depth_indicators)

    # Skill level expectations
    if skill_level == "beginner":
        if depth_score < 2:
            score -= 2
            feedback_points.append("Even beginner projects should cover testing and error handling")
    elif skill_level == "intermediate":
        if depth_score < 3:
            score -= 2
            feedback_points.append("Intermediate projects should cover testing, error handling, and architecture")
    elif skill_level == "advanced":
        if depth_score < 4:
            score -= 3
            feedback_points.append("Advanced projects should cover testing, deployment, architecture, and security")

    # Check framework sophistication
    if hasattr(plan, 'framework'):
        frameworks = [
            plan.framework.frontend,
            plan.framework.backend,
            plan.framework.storage
        ]
        frameworks = [f for f in frameworks if f]  # Remove None values

        # Beginners should have simple frameworks
        if skill_level == "beginner":
            complex_frameworks = ['React', 'Vue', 'Django', 'PostgreSQL', 'Kubernetes']
            uses_complex = any(
                any(complex in str(fw) for complex in complex_frameworks)
                for fw in frameworks
            )
            if uses_complex:
                score -= 2
                feedback_points.append("Frameworks may be too complex for beginner level - consider simpler alternatives")

        # Advanced users should use production-grade tools
        if skill_level == "advanced":
            simple_only = all(
                any(simple in str(fw).lower() for simple in ['streamlit', 'json', 'csv', 'cli'])
                for fw in frameworks
            )
            if simple_only:
                score -= 2
                feedback_points.append("Advanced projects should use more production-grade frameworks")

    # Bonus for comprehensive coverage
    if depth_score >= 5:
        feedback_points.append(f"Excellent technical breadth covering {depth_score}/6 advanced topics")
    elif depth_score >= 3:
        feedback_points.append(f"Good technical coverage with {depth_score}/6 advanced topics")

    feedback = " | ".join(feedback_points) if feedback_points else "Strong technical depth appropriate for skill level"

    return RubricScore(
        criterion=RubricCriterion.TECHNICAL_DEPTH,
        score=max(0, score),
        feedback=feedback,
        pass_threshold=6
    )


def evaluate_feasibility_for_project_type(
    plan: Any,
    project_type: str = "medium",
    time_constraint: str = "1-2 weeks"
) -> RubricScore:
    """
    Evaluate whether the project scope is feasible for the given project type and time constraint.

    This enhanced version considers:
    - Project type expectations (toy, medium, ambitious)
    - Total number of steps and phases
    - Complexity of technical requirements
    - Time constraint realism

    Args:
        plan: ProjectPlan object to evaluate
        project_type: "toy", "medium", or "ambitious"
        time_constraint: Time available (e.g., "1 week", "1-2 weeks")

    Returns:
        RubricScore for feasibility

    Teaching Note:
        Scope management is crucial. A project that's too ambitious leads to
        frustration and abandonment. Too simple leads to boredom. This function
        helps ensure the scope matches the user's time and ambition.
    """
    score = 10
    feedback_points = []

    total_steps = sum(len(phase.steps) for phase in plan.phases)
    phase_count = len(plan.phases)

    # Expected ranges by project type
    type_expectations = {
        "toy": {"min_steps": 15, "max_steps": 30, "ideal_phases": 3, "max_weeks": 1},
        "medium": {"min_steps": 35, "max_steps": 55, "ideal_phases": 5, "max_weeks": 2},
        "ambitious": {"min_steps": 50, "max_steps": 70, "ideal_phases": 5, "max_weeks": 4}
    }

    expected = type_expectations.get(project_type, type_expectations["medium"])

    # Check step count
    if total_steps < expected["min_steps"]:
        score -= 3
        feedback_points.append(
            f"{project_type.title()} projects should have {expected['min_steps']}-{expected['max_steps']} steps (found {total_steps})"
        )
    elif total_steps > expected["max_steps"]:
        score -= 2
        feedback_points.append(
            f"{total_steps} steps may be too many for {project_type} project (recommend {expected['max_steps']} max)"
        )

    # Check phase count
    if abs(phase_count - expected["ideal_phases"]) > 1:
        score -= 1
        feedback_points.append(
            f"{project_type.title()} projects typically have ~{expected['ideal_phases']} phases (found {phase_count})"
        )

    # Parse time constraint
    weeks_available = 2  # default
    if "week" in time_constraint.lower():
        if time_constraint.startswith("1 "):
            weeks_available = 1
        elif "2" in time_constraint:
            weeks_available = 2
        elif "3" in time_constraint:
            weeks_available = 3
        elif "4" in time_constraint:
            weeks_available = 4

    # Check if time is sufficient
    if weeks_available < expected["max_weeks"]:
        score -= 2
        feedback_points.append(
            f"{project_type.title()} projects typically need ~{expected['max_weeks']} weeks (only {weeks_available} available)"
        )

    # Check for deployment/production steps in toy projects
    if project_type == "toy":
        deployment_steps = [
            step for phase in plan.phases for step in phase.steps
            if any(keyword in step.title.lower() for keyword in ['deploy', 'production', 'docker', 'ci/cd'])
        ]
        if len(deployment_steps) > 2:
            score -= 1
            feedback_points.append("Toy projects should focus on core learning, not deployment complexity")

    # Check for insufficient advanced features in ambitious projects
    if project_type == "ambitious":
        advanced_features = sum(
            1 for phase in plan.phases for step in phase.steps
            if any(keyword in step.title.lower() for keyword in ['advanced', 'optimization', 'scale', 'production', 'testing'])
        )
        if advanced_features < 5:
            score -= 2
            feedback_points.append("Ambitious projects should include more advanced/production features")

    feedback = " | ".join(feedback_points) if feedback_points else f"Scope well-matched to {project_type} project with {total_steps} steps"

    return RubricScore(
        criterion=RubricCriterion.FEASIBILITY,
        score=max(0, score),
        feedback=feedback,
        pass_threshold=6
    )
