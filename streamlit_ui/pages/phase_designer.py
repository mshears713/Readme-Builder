"""
Phase Designer Agent detail page.

Displays detailed information about the PhaseDesigner agent's execution.
"""

import streamlit as st
from streamlit_ui.utils import display_phases


def render():
    """Render the Phase Designer agent page."""
    st.title("📋 Phase Designer Agent")
    st.markdown("Creates structured 5-phase build plans with ~50 implementation steps")

    st.markdown("---")

    # Agent description
    with st.expander("ℹ️ About This Agent", expanded=False):
        st.markdown("""
        **Purpose:** Designs a complete build plan organized into 5 phases with specific implementation steps.

        **What it does:**
        - Creates 5 logical phases (e.g., Setup, Core Features, Advanced Features, Polish, Deployment)
        - Generates ~10 steps per phase (~50 total steps)
        - Defines clear step titles and descriptions
        - Establishes dependencies between steps
        - Ensures phases build on each other logically

        **Input:**
        - `ProjectIdea` from ConceptExpander
        - `ProjectGoals` from GoalsAnalyzer
        - `FrameworkChoice` from FrameworkSelector

        **Output:**
        - List of `Phase` objects, each containing:
            - `index`: Phase number (1-5)
            - `name`: Descriptive phase name
            - `description`: What this phase accomplishes
            - `steps`: List of Step objects with:
                - `index`: Global step number
                - `title`: Step name
                - `description`: What to build
                - `dependencies`: Prerequisites

        **Model:** Uses LLM with project planning expertise
        """)

    st.markdown("---")

    # Check if agent has completed
    if not st.session_state.get("PhaseDesigner_completed", False):
        st.info("⏸️ This agent hasn't run yet. Go to Home page to start execution.")
        return

    # Display execution status
    col1, col2, col3 = st.columns(3)
    with col1:
        st.success("✅ Agent Completed")
    with col2:
        if st.session_state.get("phases"):
            phase_count = len(st.session_state.phases)
            st.metric("Phases Created", phase_count)
    with col3:
        if st.session_state.get("phases"):
            step_count = sum(len(p.steps) for p in st.session_state.phases)
            st.metric("Total Steps", step_count)

    st.markdown("---")

    # Display in sections
    tab1, tab2, tab3, tab4 = st.tabs(["📥 Input", "🔄 Processing", "📤 Output", "🔍 Logs"])

    with tab1:
        st.subheader("Input Received")

        # Display all previous outputs that feed into this agent
        col1, col2 = st.columns(2)

        with col1:
            if st.session_state.get("project_idea"):
                st.write("**Project Concept:**")
                st.info(st.session_state.project_idea.refined_summary)

        with col2:
            if st.session_state.get("framework_choice"):
                st.write("**Technology Stack:**")
                framework = st.session_state.framework_choice
                tech_list = [
                    framework.frontend or "",
                    framework.backend or "",
                    framework.storage or ""
                ]
                tech_str = ", ".join([t for t in tech_list if t])
                st.info(tech_str)

        if st.session_state.get("project_goals"):
            st.write("**Goals to Achieve:**")
            goals = st.session_state.project_goals
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Learning Goals", len(goals.learning_goals))
            with col2:
                st.metric("Technical Goals", len(goals.technical_goals))

    with tab2:
        st.subheader("Agent Processing")

        st.markdown("""
        **Processing Steps:**

        1. **Analyze Project Scope**: Reviews concept, goals, and tech stack
        2. **Design Phase Structure**: Creates 5 logical phases
        3. **Generate Steps**: Creates ~10 implementation steps per phase
        4. **Set Dependencies**: Identifies which steps depend on others
        5. **Validate Flow**: Ensures phases build on each other logically
        6. **Balance Complexity**: Distributes work evenly across phases
        7. **Verify Completeness**: Confirms all goals are addressed
        """)

        if st.session_state.get("phases"):
            phases = st.session_state.phases

            st.write("**Phase Distribution:**")

            # Show step distribution across phases
            for phase in phases:
                st.write(f"**Phase {phase.index}: {phase.name}** - {len(phase.steps)} steps")

            st.info("""
            The agent structured the project into distinct phases, each with a clear
            purpose and set of deliverables. Steps are ordered to ensure dependencies
            are built before dependent features.
            """)

    with tab3:
        st.subheader("Agent Output")

        # Display the phases with all details
        if st.session_state.get("phases"):
            display_phases(st.session_state.phases)

            # Show dependency graph summary
            phases = st.session_state.phases
            all_steps = [step for phase in phases for step in phase.steps]
            steps_with_deps = [s for s in all_steps if s.dependencies]

            st.markdown("---")
            st.write("**Dependency Analysis:**")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Steps", len(all_steps))
            with col2:
                st.metric("Steps with Dependencies", len(steps_with_deps))
            with col3:
                avg_deps = sum(len(s.dependencies) for s in steps_with_deps) / max(len(steps_with_deps), 1)
                st.metric("Avg Dependencies", f"{avg_deps:.1f}")

            # Show critical path hint
            if steps_with_deps:
                st.info("""
                📊 **Critical Path**: Steps with dependencies must be completed in order.
                This ensures foundational work is done before building advanced features.
                """)
        else:
            st.warning("No output data available")

    with tab4:
        st.subheader("Agent Logs")

        # Display agent-specific logs
        if st.session_state.get("agent_logs", {}).get("PhaseDesigner"):
            logs = st.session_state.agent_logs["PhaseDesigner"]
            for log in logs:
                st.text(f"[{log['timestamp']}] {log['message']}")
        else:
            st.info("No agent-specific logs available")
