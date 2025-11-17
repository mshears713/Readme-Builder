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
