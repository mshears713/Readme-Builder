"""
Concept Expander Agent detail page.

This page displays detailed information about the ConceptExpander agent:
- Input: Raw project idea
- Processing: Concept refinement and constraint extraction
- Output: ProjectIdea with refined summary and constraints
- Reasoning: How the agent transformed the raw idea
"""

import streamlit as st
from streamlit_ui.utils import display_project_idea


def render():
    """Render the Concept Expander agent page."""
    st.title("📝 Concept Expander Agent")
    st.markdown("Refines raw project ideas into structured, clear concepts")

    st.markdown("---")

    # Agent description
    with st.expander("ℹ️ About This Agent", expanded=False):
        st.markdown("""
        **Purpose:** Takes raw, potentially vague project ideas and expands them into clear, structured concepts.

        **What it does:**
        - Removes noise and ambiguity from user input
        - Adds context and clarity
        - Extracts project constraints (time, complexity, hardware requirements)
        - Ensures the concept is actionable for downstream agents

        **Input:**
        - Raw project description (user's text input)

        **Output:**
        - `ProjectIdea` object with:
            - `raw_description`: Original user input
            - `refined_summary`: Cleaned, expanded version with full context
            - `constraints`: Dictionary of project constraints

        **Model:** Uses LLM to understand intent and expand ideas
        """)

    st.markdown("---")

    # Check if agent has completed
    if not st.session_state.get("ConceptExpander_completed", False):
        st.info("⏸️ This agent hasn't run yet. Go to Home page to start execution.")
        return

    # Display execution status
    col1, col2 = st.columns(2)
    with col1:
        st.success("✅ Agent Completed")
    with col2:
        if st.session_state.get("agent_logs", {}).get("ConceptExpander"):
            log_count = len(st.session_state.agent_logs["ConceptExpander"])
            st.info(f"📋 {log_count} log entries")

    st.markdown("---")

    # Display in sections
    tab1, tab2, tab3, tab4 = st.tabs(["📥 Input", "🔄 Processing", "📤 Output", "🔍 Logs"])

    with tab1:
        st.subheader("Input Received")

        # Display raw idea
        if st.session_state.get("raw_idea"):
            st.write("**Raw Project Idea:**")
            st.info(st.session_state.raw_idea)

            # Display metadata
            st.write("**Configuration:**")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Skill Level", st.session_state.get("skill_level", "N/A"))
            with col2:
                st.metric("Phase", st.session_state.get("phase", "N/A"))
        else:
            st.warning("No input data available")

    with tab2:
        st.subheader("Agent Processing")

        st.markdown("""
        **Processing Steps:**

        1. **Parse Input**: Receives raw project description from user
        2. **Analyze Intent**: Uses LLM to understand what the user wants to build
        3. **Expand Context**: Adds missing details and clarifies vague points
        4. **Extract Constraints**: Identifies time, complexity, and technical constraints
        5. **Generate Refined Summary**: Creates a clear, actionable project description
        6. **Structure Output**: Formats result as ProjectIdea dataclass
        """)

        # Show reasoning if available
        if st.session_state.get("project_idea"):
            st.write("**Reasoning:**")
            st.info("""
            The agent analyzed the raw idea and:
            - Identified key project components
            - Clarified technical requirements
            - Assessed project scope and complexity
            - Structured the concept for downstream agents
            """)

        # Show constraints extraction
        if st.session_state.get("project_idea") and st.session_state.project_idea.constraints:
            st.write("**Constraints Identified:**")
            for key, value in st.session_state.project_idea.constraints.items():
                st.write(f"- **{key.replace('_', ' ').title()}:** {value}")

    with tab3:
        st.subheader("Agent Output")

        # Display the ProjectIdea
        if st.session_state.get("project_idea"):
            display_project_idea(st.session_state.project_idea)

            # Show comparison
            st.markdown("---")
            st.write("**Before & After Comparison:**")
            col1, col2 = st.columns(2)

            with col1:
                st.write("**Original (Raw):**")
                st.text_area(
                    "Raw idea",
                    value=st.session_state.raw_idea,
                    height=150,
                    disabled=True,
                    label_visibility="collapsed"
                )

            with col2:
                st.write("**Refined:**")
                st.text_area(
                    "Refined summary",
                    value=st.session_state.project_idea.refined_summary,
                    height=150,
                    disabled=True,
                    label_visibility="collapsed"
                )

            # Show quality score if available
            if st.session_state.get("clarity_score"):
                st.markdown("---")
                st.write("**Quality Assessment:**")
                score = st.session_state.clarity_score
                if hasattr(score, 'score'):
                    st.metric("Clarity Score", f"{score.score}/10")
                    if hasattr(score, 'feedback'):
                        st.info(score.feedback)
        else:
            st.warning("No output data available")

    with tab4:
        st.subheader("Agent Logs")

        # Display agent-specific logs
        if st.session_state.get("agent_logs", {}).get("ConceptExpander"):
            logs = st.session_state.agent_logs["ConceptExpander"]
            for log in logs:
                st.text(f"[{log['timestamp']}] {log['message']}")
        else:
            st.info("No agent-specific logs available")

        # Show captured stdout/stderr if available
        if st.session_state.get("captured_stdout"):
            with st.expander("Show Captured Output"):
                st.code(st.session_state.captured_stdout, language="text")
