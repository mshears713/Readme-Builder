"""
Framework Selector Agent detail page.

Displays detailed information about the FrameworkSelector agent's execution.
"""

import streamlit as st
from streamlit_ui.utils import display_framework_choice, display_project_goals


def render():
    """Render the Framework Selector agent page."""
    st.title("🔧 Framework Selector Agent")
    st.markdown("Recommends technology stacks based on project goals and skill level")

    st.markdown("---")

    # Agent description
    with st.expander("ℹ️ About This Agent", expanded=False):
        st.markdown("""
        **Purpose:** Chooses appropriate frameworks and libraries that match project goals and skill level.

        **What it does:**
        - Selects frontend framework (Streamlit, Flask+HTML, CLI-only, etc.)
        - Chooses backend/API framework (FastAPI, Flask, Django, None)
        - Recommends storage solution (SQLite, PostgreSQL, JSON files, etc.)
        - Suggests domain-specific libraries (CrewAI, LangChain, BeautifulSoup, etc.)
        - Ensures choices are beginner-friendly for lower skill levels

        **Input:**
        - `ProjectIdea` from ConceptExpander
        - `ProjectGoals` from GoalsAnalyzer
        - Skill level configuration

        **Output:**
        - `FrameworkChoice` object with:
            - `frontend`: UI framework or None
            - `backend`: Server framework or None
            - `storage`: Data persistence approach
            - `special_libs`: List of domain-specific libraries

        **Model:** Uses LLM with framework knowledge and skill level templates
        """)

    st.markdown("---")

    # Check if agent has completed
    if not st.session_state.get("FrameworkSelector_completed", False):
        st.info("⏸️ This agent hasn't run yet. Go to Home page to start execution.")
        return

    # Display execution status
    col1, col2 = st.columns(2)
    with col1:
        st.success("✅ Agent Completed")
    with col2:
        if st.session_state.get("agent_logs", {}).get("FrameworkSelector"):
            log_count = len(st.session_state.agent_logs["FrameworkSelector"])
            st.info(f"📋 {log_count} log entries")

    st.markdown("---")

    # Display in sections
    tab1, tab2, tab3, tab4 = st.tabs(["📥 Input", "🔄 Processing", "📤 Output", "🔍 Logs"])

    with tab1:
        st.subheader("Input Received")

        # Display project goals
        if st.session_state.get("project_goals"):
            display_project_goals(st.session_state.project_goals)

            st.markdown("---")
            st.write("**Configuration:**")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Skill Level", st.session_state.get("skill_level", "N/A").title())
            with col2:
                st.metric("Project Type", st.session_state.get("project_type", "general").title())
        else:
            st.warning("No input data available")

    with tab2:
        st.subheader("Agent Processing")

        st.markdown("""
        **Processing Steps:**

        1. **Analyze Requirements**: Reviews project goals and technical needs
        2. **Assess Skill Level**: Considers user's programming experience
        3. **Match Frontend**: Chooses UI framework or determines if CLI-only
        4. **Select Backend**: Picks server/API framework if needed
        5. **Choose Storage**: Recommends appropriate data persistence
        6. **Add Special Libraries**: Identifies domain-specific tools needed
        7. **Validate Stack**: Ensures all choices work well together
        """)

        # Show framework selection reasoning
        if st.session_state.get("framework_choice"):
            framework = st.session_state.framework_choice

            st.write("**Selection Reasoning:**")

            reasons = []
            if framework.frontend:
                reasons.append(f"**Frontend ({framework.frontend})**: Selected for rapid UI development")
            if framework.backend:
                reasons.append(f"**Backend ({framework.backend})**: Chosen for API/server needs")
            if framework.storage:
                reasons.append(f"**Storage ({framework.storage})**: Appropriate for data scale and complexity")
            if framework.special_libs:
                lib_list = ", ".join(framework.special_libs)
                reasons.append(f"**Libraries ({lib_list})**: Domain-specific tools for project requirements")

            for reason in reasons:
                st.info(reason)

    with tab3:
        st.subheader("Agent Output")

        # Display the FrameworkChoice
        if st.session_state.get("framework_choice"):
            display_framework_choice(st.session_state.framework_choice)

            framework = st.session_state.framework_choice

            # Technology stack visualization
            st.markdown("---")
            st.write("**Complete Technology Stack:**")

            # Create a visual stack diagram
            stack_layers = []

            if framework.frontend:
                stack_layers.append(("🎨 Frontend", framework.frontend))
            if framework.backend:
                stack_layers.append(("⚙️ Backend", framework.backend))
            if framework.storage:
                stack_layers.append(("💾 Storage", framework.storage))

            for emoji, tech in stack_layers:
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.write(emoji)
                with col2:
                    st.code(tech, language="text")

            if framework.special_libs:
                st.write("**📚 Additional Libraries:**")
                for lib in framework.special_libs:
                    st.write(f"• {lib}")

            # Show compatibility notes
            st.markdown("---")
            st.success("""
            ✅ **Stack Compatibility**: All selected technologies are compatible and
            work well together for this project type and skill level.
            """)
        else:
            st.warning("No output data available")

    with tab4:
        st.subheader("Agent Logs")

        # Display agent-specific logs
        if st.session_state.get("agent_logs", {}).get("FrameworkSelector"):
            logs = st.session_state.agent_logs["FrameworkSelector"]
            for log in logs:
                st.text(f"[{log['timestamp']}] {log['message']}")
        else:
            st.info("No agent-specific logs available")
