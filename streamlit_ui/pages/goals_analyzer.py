"""
Goals Analyzer Agent detail page.

Displays detailed information about the GoalsAnalyzer agent's execution.
"""

import streamlit as st
from streamlit_ui.utils import display_project_goals, display_project_idea


def render():
    """Render the Goals Analyzer agent page."""
    st.title("🎯 Goals Analyzer Agent")
    st.markdown("Extracts learning and technical objectives from project concepts")

    st.markdown("---")

    # Agent description
    with st.expander("ℹ️ About This Agent", expanded=False):
        st.markdown("""
        **Purpose:** Analyzes the refined project concept and extracts clear learning and technical goals.

        **What it does:**
        - Identifies what skills/concepts the user will learn
        - Extracts specific technical deliverables to build
        - Prioritizes goals based on educational value
        - Ensures goals align with skill level

        **Input:**
        - `ProjectIdea` from ConceptExpander

        **Output:**
        - `ProjectGoals` object with:
            - `learning_goals`: List of concepts to learn (e.g., "async programming", "REST APIs")
            - `technical_goals`: List of deliverables (e.g., "web scraper", "API endpoint")
            - `priority_notes`: Guidance on which goals are most important

        **Model:** Uses LLM to extract educational and technical objectives
        """)

    st.markdown("---")

    # Check if agent has completed
    if not st.session_state.get("GoalsAnalyzer_completed", False):
        st.info("⏸️ This agent hasn't run yet. Go to Home page to start execution.")
        return

    # Display execution status
    col1, col2 = st.columns(2)
    with col1:
        st.success("✅ Agent Completed")
    with col2:
        if st.session_state.get("agent_logs", {}).get("GoalsAnalyzer"):
            log_count = len(st.session_state.agent_logs["GoalsAnalyzer"])
            st.info(f"📋 {log_count} log entries")

    st.markdown("---")

    # Display in sections
    tab1, tab2, tab3, tab4 = st.tabs(["📥 Input", "🔄 Processing", "📤 Output", "🔍 Logs"])

    with tab1:
        st.subheader("Input Received")

        # Display the ProjectIdea that was input to this agent
        if st.session_state.get("project_idea"):
            st.write("**Project Concept (from ConceptExpander):**")
            display_project_idea(st.session_state.project_idea)
        else:
            st.warning("No input data available")

    with tab2:
        st.subheader("Agent Processing")

        st.markdown("""
        **Processing Steps:**

        1. **Analyze Project Concept**: Reviews refined project summary
        2. **Extract Learning Objectives**: Identifies concepts and skills to learn
        3. **Identify Technical Goals**: Determines specific technical deliverables
        4. **Prioritize Goals**: Ranks goals by educational value and importance
        5. **Validate Alignment**: Ensures goals match the specified skill level
        6. **Structure Output**: Formats result as ProjectGoals dataclass
        """)

        # Show goal extraction reasoning
        if st.session_state.get("project_goals"):
            goals = st.session_state.project_goals

            st.write("**Goal Extraction Summary:**")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Learning Goals", len(goals.learning_goals))
            with col2:
                st.metric("Technical Goals", len(goals.technical_goals))

            st.info("""
            The agent analyzed the project concept to identify:
            - Core technical skills needed
            - Programming concepts to learn
            - Specific deliverables to build
            - Priority and sequencing of goals
            """)

    with tab3:
        st.subheader("Agent Output")

        # Display the ProjectGoals
        if st.session_state.get("project_goals"):
            display_project_goals(st.session_state.project_goals)

            # Show goal breakdown
            goals = st.session_state.project_goals

            if goals.learning_goals and goals.technical_goals:
                st.markdown("---")
                st.write("**Goal Mapping:**")

                st.write("This project combines:")
                st.write(f"- **{len(goals.learning_goals)}** learning objectives (concepts to master)")
                st.write(f"- **{len(goals.technical_goals)}** technical deliverables (things to build)")

                if goals.priority_notes:
                    st.success(f"**Priority Guidance:** {goals.priority_notes}")
        else:
            st.warning("No output data available")

    with tab4:
        st.subheader("Agent Logs")

        # Display agent-specific logs
        if st.session_state.get("agent_logs", {}).get("GoalsAnalyzer"):
            logs = st.session_state.agent_logs["GoalsAnalyzer"]
            for log in logs:
                st.text(f"[{log['timestamp']}] {log['message']}")
        else:
            st.info("No agent-specific logs available")
