"""
Utility functions for the Streamlit UI.

This module provides helper functions for session state management,
data formatting, and common UI components.
"""

import streamlit as st
from datetime import datetime
from typing import Optional, Dict, Any, List
import io
import sys
from contextlib import redirect_stdout, redirect_stderr


def initialize_session_state():
    """
    Initialize Streamlit session state with default values.

    This function sets up all the necessary session state variables
    for tracking execution progress, agent outputs, and UI state.
    """
    defaults = {
        # Execution state
        "execution_should_start": False,
        "execution_started": False,
        "execution_completed": False,
        "execution_error": None,
        "start_time": None,
        "end_time": None,

        # Input parameters
        "raw_idea": "",
        "skill_level": "intermediate",
        "project_type": "general",
        "phase": 4,  # Default to complete pipeline
        "max_iterations": 2,
        "verbose": True,

        # Current execution status
        "current_agent": "Not started",
        "progress_percent": 0,

        # Agent completion flags
        "ConceptExpander_completed": False,
        "GoalsAnalyzer_completed": False,
        "FrameworkSelector_completed": False,
        "PhaseDesigner_completed": False,
        "TeacherAgent_completed": False,
        "EvaluatorAgent_completed": False,
        "PRDWriter_completed": False,

        # Agent outputs
        "project_idea": None,
        "project_goals": None,
        "framework_choice": None,
        "phases": None,
        "enriched_phases": None,
        "evaluation_result": None,
        "readme_content": None,
        "project_name": None,

        # Results from orchestration
        "planning_result": None,
        "full_plan_result": None,
        "final_result": None,

        # Metadata
        "iterations": 0,
        "clarity_score": None,

        # Logs and debugging
        "execution_logs": [],
        "agent_logs": {},
        "captured_stdout": "",
        "captured_stderr": "",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_execution_state():
    """Reset the execution state for a new run."""
    keys_to_reset = [
        "execution_should_start", "execution_started", "execution_completed", "execution_error",
        "start_time", "end_time", "current_agent", "progress_percent",
        "ConceptExpander_completed", "GoalsAnalyzer_completed",
        "FrameworkSelector_completed", "PhaseDesigner_completed",
        "TeacherAgent_completed", "EvaluatorAgent_completed",
        "PRDWriter_completed", "project_idea", "project_goals",
        "framework_choice", "phases", "enriched_phases",
        "evaluation_result", "readme_content", "project_name",
        "planning_result", "full_plan_result", "final_result",
        "iterations", "clarity_score", "execution_logs", "agent_logs",
        "captured_stdout", "captured_stderr"
    ]

    for key in keys_to_reset:
        if key in ["execution_logs", "agent_logs"]:
            st.session_state[key] = [] if key == "execution_logs" else {}
        elif key in ["captured_stdout", "captured_stderr"]:
            st.session_state[key] = ""
        else:
            st.session_state[key] = None if "_completed" not in key else False

    st.session_state["progress_percent"] = 0
    st.session_state["current_agent"] = "Not started"


def add_log(message: str, level: str = "INFO"):
    """
    Add a log message to the execution logs.

    Args:
        message: The log message
        level: Log level (DEBUG, INFO, WARNING, ERROR)
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {
        "timestamp": timestamp,
        "level": level,
        "message": message
    }
    st.session_state.execution_logs.append(log_entry)


def add_agent_log(agent_name: str, log_message: str):
    """
    Add a log message specific to an agent.

    Args:
        agent_name: Name of the agent
        log_message: The log message
    """
    if agent_name not in st.session_state.agent_logs:
        st.session_state.agent_logs[agent_name] = []

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.agent_logs[agent_name].append({
        "timestamp": timestamp,
        "message": log_message
    })


def update_progress(agent_name: str, progress: int):
    """
    Update the current execution progress.

    Args:
        agent_name: Name of the currently executing agent
        progress: Progress percentage (0-100)
    """
    st.session_state.current_agent = agent_name
    st.session_state.progress_percent = progress
    add_log(f"Agent {agent_name} - Progress: {progress}%", "INFO")


def mark_agent_completed(agent_name: str):
    """
    Mark an agent as completed.

    Args:
        agent_name: Name of the completed agent
    """
    st.session_state[f"{agent_name}_completed"] = True
    add_log(f"Agent {agent_name} completed", "INFO")


def get_elapsed_time() -> Optional[str]:
    """
    Get the elapsed time since execution started.

    Returns:
        Formatted elapsed time string or None if not started
    """
    if not st.session_state.start_time:
        return None

    end = st.session_state.end_time or datetime.now()
    elapsed = end - st.session_state.start_time
    seconds = int(elapsed.total_seconds())
    minutes = seconds // 60
    seconds = seconds % 60

    if minutes > 0:
        return f"{minutes}m {seconds}s"
    return f"{seconds}s"


def display_project_idea(idea):
    """Display ProjectIdea in a formatted way."""
    if not idea:
        st.info("No concept data available yet.")
        return

    st.subheader("Project Concept")
    st.write("**Refined Summary:**")
    st.write(idea.refined_summary)

    if idea.constraints:
        st.write("**Constraints:**")
        cols = st.columns(min(len(idea.constraints), 4))
        for idx, (key, value) in enumerate(idea.constraints.items()):
            with cols[idx % len(cols)]:
                st.metric(key.replace("_", " ").title(), str(value))


def display_project_goals(goals):
    """Display ProjectGoals in a formatted way."""
    if not goals:
        st.info("No goals data available yet.")
        return

    st.subheader("Learning & Technical Goals")
    col1, col2 = st.columns(2)

    with col1:
        st.write("**Learning Goals:**")
        if goals.learning_goals:
            for i, goal in enumerate(goals.learning_goals, 1):
                st.write(f"{i}. {goal}")
        else:
            st.write("_No learning goals defined_")

    with col2:
        st.write("**Technical Goals:**")
        if goals.technical_goals:
            for i, goal in enumerate(goals.technical_goals, 1):
                st.write(f"{i}. {goal}")
        else:
            st.write("_No technical goals defined_")

    if goals.priority_notes:
        st.info(f"**Priority:** {goals.priority_notes}")


def display_framework_choice(framework):
    """Display FrameworkChoice in a formatted way."""
    if not framework:
        st.info("No framework data available yet.")
        return

    st.subheader("Technology Stack")
    cols = st.columns(4)

    with cols[0]:
        st.metric("Frontend", framework.frontend or "None")
    with cols[1]:
        st.metric("Backend", framework.backend or "None")
    with cols[2]:
        st.metric("Storage", framework.storage or "None")
    with cols[3]:
        if framework.special_libs:
            st.write("**Special Libraries:**")
            for lib in framework.special_libs:
                st.write(f"• {lib}")
        else:
            st.write("_No special libraries_")


def display_phases(phases):
    """Display Phase list in a formatted way."""
    if not phases:
        st.info("No phases data available yet.")
        return

    st.subheader(f"Project Structure ({len(phases)} Phases)")

    for phase in phases:
        with st.expander(
            f"**Phase {phase.index}: {phase.name}** ({len(phase.steps)} steps)",
            expanded=False
        ):
            st.write(phase.description)
            st.markdown("---")

            for step in phase.steps:
                st.write(f"**Step {step.index}: {step.title}**")
                st.write(step.description)

                if step.what_you_learn:
                    st.info(f"📚 **What You Learn:** {step.what_you_learn}")

                if step.dependencies:
                    deps = ", ".join(str(d) for d in step.dependencies)
                    st.caption(f"📌 Dependencies: Steps {deps}")

                st.markdown("---")


def display_evaluation_result(evaluation):
    """Display EvaluationResult in a formatted way."""
    if not evaluation:
        st.info("No evaluation data available yet.")
        return

    st.subheader("Quality Evaluation")

    # Approval status
    if evaluation.approved:
        st.success("✅ Plan Approved!")
    else:
        st.error("❌ Plan Needs Revision")

    # Scores
    if hasattr(evaluation, 'scores') and evaluation.scores:
        st.write("**Quality Scores:**")
        cols = st.columns(len(evaluation.scores))

        for idx, (criterion, score) in enumerate(evaluation.scores.items()):
            with cols[idx]:
                # Extract criterion name
                criterion_name = str(criterion).split(".")[-1].replace("_", " ").title()

                # Get score value
                score_value = score.score if hasattr(score, 'score') else score

                # Display metric
                st.metric(
                    criterion_name,
                    f"{score_value}/10"
                )

                # Display feedback if available
                if hasattr(score, 'feedback') and score.feedback:
                    st.caption(score.feedback)

    # Display overall feedback
    if hasattr(evaluation, 'feedback') and evaluation.feedback:
        st.write("**Overall Feedback:**")
        st.info(evaluation.feedback)

    # Critical issues
    if hasattr(evaluation, 'critical_issues') and evaluation.critical_issues:
        st.error("**Critical Issues:**")
        for issue in evaluation.critical_issues:
            st.write(f"• {issue}")

    # Suggestions
    if hasattr(evaluation, 'suggestions') and evaluation.suggestions:
        st.warning("**Suggestions:**")
        for suggestion in evaluation.suggestions:
            st.write(f"• {suggestion}")


def display_readme_preview(readme_content: str, max_lines: int = 50):
    """
    Display a preview of the README content.

    Args:
        readme_content: The markdown content
        max_lines: Maximum number of lines to show in preview
    """
    if not readme_content:
        st.info("No README content available yet.")
        return

    st.subheader("README Preview")

    # Action buttons
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("📋 Copy to Clipboard"):
            st.code(readme_content, language="markdown")
            st.success("Content displayed above - you can copy it!")
    with col2:
        if st.button("📥 Download"):
            st.download_button(
                label="Download README.md",
                data=readme_content,
                file_name="README.md",
                mime="text/markdown"
            )

    # Display preview
    lines = readme_content.split('\n')
    if len(lines) > max_lines:
        preview = '\n'.join(lines[:max_lines])
        st.markdown(preview)
        st.info(f"Showing first {max_lines} lines. Click 'Full View' below to see all {len(lines)} lines.")

        if st.checkbox("Show Full Content"):
            st.markdown(readme_content)
    else:
        st.markdown(readme_content)


def format_dict_display(data: Dict[str, Any]) -> str:
    """
    Format a dictionary for nice display.

    Args:
        data: Dictionary to format

    Returns:
        Formatted string
    """
    lines = []
    for key, value in data.items():
        formatted_key = key.replace("_", " ").title()
        lines.append(f"**{formatted_key}:** {value}")
    return "\n\n".join(lines)


class CaptureOutput:
    """Context manager to capture stdout and stderr."""

    def __init__(self):
        self.stdout = io.StringIO()
        self.stderr = io.StringIO()

    def __enter__(self):
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr
        sys.stdout = self.stdout
        sys.stderr = self.stderr
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr

    def get_stdout(self):
        return self.stdout.getvalue()

    def get_stderr(self):
        return self.stderr.getvalue()
