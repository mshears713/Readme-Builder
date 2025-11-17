"""
Teacher Agent detail page.

Displays detailed information about the TeacherAgent's execution.
"""

import streamlit as st


def render():
    """Render the Teacher Agent page."""
    st.title("👨‍🏫 Teacher Agent")
    st.markdown("Enriches implementation steps with pedagogical annotations")

    st.markdown("---")

    # Agent description
    with st.expander("ℹ️ About This Agent", expanded=False):
        st.markdown("""
        **Purpose:** Adds educational value by annotating each step with learning explanations.

        **What it does:**
        - Reviews each implementation step from PhaseDesigner
        - Adds "what you learn" annotations explaining concepts
        - Provides pedagogical context for why each step matters
        - Ensures explanations match the user's skill level
        - Creates a learning arc through the project

        **Input:**
        - List of `Phase` objects from PhaseDesigner
        - Skill level configuration

        **Output:**
        - Enriched `Phase` objects where each `Step` now has:
            - `what_you_learn`: Explanation of concepts learned in this step
            - Enhanced descriptions with learning context

        **Model:** Uses LLM with teaching expertise and educational scaffolding
        """)

    st.markdown("---")

    # Check if agent has completed
    if not st.session_state.get("TeacherAgent_completed", False):
        st.info("⏸️ This agent hasn't run yet. Go to Home page to start execution.")
        return

    # Display execution status
    col1, col2, col3 = st.columns(3)
    with col1:
        st.success("✅ Agent Completed")
    with col2:
        if st.session_state.get("phases"):
            all_steps = [s for p in st.session_state.phases for s in p.steps]
            annotated = [s for s in all_steps if s.what_you_learn]
            st.metric("Steps Annotated", len(annotated))
    with col3:
        if st.session_state.get("agent_logs", {}).get("TeacherAgent"):
            log_count = len(st.session_state.agent_logs["TeacherAgent"])
            st.info(f"📋 {log_count} log entries")

    st.markdown("---")

    # Display in sections
    tab1, tab2, tab3, tab4 = st.tabs(["📥 Input", "🔄 Processing", "📤 Output", "🔍 Logs"])

    with tab1:
        st.subheader("Input Received")

        # Display phases before teaching enrichment
        if st.session_state.get("phases"):
            phases = st.session_state.phases
            st.write(f"**Phases to Enrich:** {len(phases)}")

            total_steps = sum(len(p.steps) for p in phases)
            st.write(f"**Total Steps:** {total_steps}")

            st.write("**Phase Overview:**")
            for phase in phases:
                st.write(f"- Phase {phase.index}: {phase.name} ({len(phase.steps)} steps)")

            st.info("""
            The Teacher Agent receives the complete phase structure and adds
            educational annotations to each step.
            """)
        else:
            st.warning("No input data available")

    with tab2:
        st.subheader("Agent Processing")

        st.markdown("""
        **Processing Steps:**

        1. **Review Step Descriptions**: Analyzes what each step accomplishes technically
        2. **Identify Learning Opportunities**: Determines what concepts are taught
        3. **Write Pedagogical Annotations**: Creates "what you learn" explanations
        4. **Match Skill Level**: Adjusts explanation depth to user experience
        5. **Create Learning Arc**: Ensures concepts build on each other
        6. **Add Context**: Explains why each step matters in the bigger picture
        7. **Validate Clarity**: Ensures explanations are clear and helpful
        """)

        if st.session_state.get("phases"):
            st.write("**Teaching Strategy:**")

            st.info("""
            The agent approaches teaching through:
            - **Concept Introduction**: New ideas are explained when first encountered
            - **Progressive Complexity**: Simple concepts before advanced ones
            - **Practical Context**: Theory tied to specific implementation
            - **Skill Building**: Each step reinforces previous learning
            """)

            # Show sample learning progression
            phases = st.session_state.phases
            all_steps = [s for p in phases for s in p.steps if s.what_you_learn]

            if all_steps:
                st.write("**Sample Learning Progression:**")
                sample_steps = all_steps[:3]  # Show first 3 as examples

                for step in sample_steps:
                    with st.expander(f"Step {step.index}: {step.title}"):
                        st.write(f"**Task:** {step.description}")
                        st.success(f"**📚 What You Learn:** {step.what_you_learn}")

    with tab3:
        st.subheader("Agent Output")

        # Display enriched phases with teaching annotations
        if st.session_state.get("phases"):
            phases = st.session_state.phases

            st.write("**Enriched Project Plan with Learning Annotations:**")

            # Show statistics
            all_steps = [s for p in phases for s in p.steps]
            annotated_steps = [s for s in all_steps if s.what_you_learn]

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Steps", len(all_steps))
            with col2:
                st.metric("Annotated", len(annotated_steps))
            with col3:
                coverage = (len(annotated_steps) / max(len(all_steps), 1)) * 100
                st.metric("Coverage", f"{coverage:.0f}%")

            # Display each phase with emphasis on learning
            for phase in phases:
                with st.expander(
                    f"**Phase {phase.index}: {phase.name}** ({len(phase.steps)} steps)",
                    expanded=False
                ):
                    st.write(f"**Phase Goal:** {phase.description}")
                    st.markdown("---")

                    for step in phase.steps:
                        st.write(f"**Step {step.index}: {step.title}**")
                        st.write(step.description)

                        if step.what_you_learn:
                            st.success(f"📚 **What You Learn:** {step.what_you_learn}")
                        else:
                            st.warning("No learning annotation for this step")

                        if step.dependencies:
                            deps = ", ".join(str(d) for d in step.dependencies)
                            st.caption(f"📌 Prerequisites: Steps {deps}")

                        st.markdown("---")

            # Show learning themes
            st.markdown("---")
            st.write("**Educational Value:**")
            st.info("""
            Every step now includes pedagogical context that:
            - Explains what concepts are being learned
            - Connects implementation to theory
            - Builds a progressive learning experience
            - Helps learners understand the "why" behind each task
            """)
        else:
            st.warning("No output data available")

    with tab4:
        st.subheader("Agent Logs")

        # Display agent-specific logs
        if st.session_state.get("agent_logs", {}).get("TeacherAgent"):
            logs = st.session_state.agent_logs["TeacherAgent"]
            for log in logs:
                st.text(f"[{log['timestamp']}] {log['message']}")
        else:
            st.info("No agent-specific logs available")
