"""
Teacher Agent detail page.

Displays detailed information about the TeacherAgent's execution.
"""

import streamlit as st


def render():
    """Render the Teacher Agent page."""
    st.title("👨‍🏫 Teacher Agent")
    st.markdown("Guides implementing agents to build educational features into programs")

    st.markdown("---")

    # Agent description
    with st.expander("ℹ️ About This Agent", expanded=False):
        st.markdown("""
        **Purpose:** Instructs implementing AI agents on what educational features to build into the program.

        **What it does:**
        - Reviews each implementation step from PhaseDesigner
        - Adds "teaching guidance" specifying educational features to include
        - Instructs the agent to build tooltips, documentation, examples, and interactive demos
        - Ensures the final program helps users learn through interaction
        - Creates a program that teaches its users

        **Input:**
        - List of `Phase` objects from PhaseDesigner
        - Target user skill level for the final program

        **Output:**
        - Enriched `Phase` objects where each `Step` now has:
            - `teaching_guidance`: Instructions for what educational elements to build
            - Guidance on tooltips, examples, help sections, etc.

        **Model:** Uses LLM with educational product design expertise
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
            annotated = [s for s in all_steps if s.teaching_guidance]
            st.metric("Steps with Guidance", len(annotated))
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
        2. **Identify Educational Opportunities**: Determines what features could help users learn
        3. **Design Educational Features**: Specifies tooltips, examples, docs, demos to build
        4. **Match Target Audience**: Adjusts features to user skill level
        5. **Create Coherent Experience**: Ensures educational features work together
        6. **Specify Concrete Elements**: Provides clear instructions on what to build
        7. **Validate Practicality**: Ensures guidance is actionable for implementing agent
        """)

        if st.session_state.get("phases"):
            st.write("**Educational Strategy:**")

            st.info("""
            The agent instructs the implementing agent to:
            - **Add Interactive Elements**: Tooltips, hover hints, guided tours
            - **Include Examples**: Code samples, demos, use case scenarios
            - **Build Documentation**: Inline help, README sections, contextual guidance
            - **Create Learning Paths**: Progressive disclosure, tutorials, walkthroughs
            """)

            # Show sample guidance
            phases = st.session_state.phases
            all_steps = [s for p in phases for s in p.steps if s.teaching_guidance]

            if all_steps:
                st.write("**Sample Educational Guidance:**")
                sample_steps = all_steps[:3]  # Show first 3 as examples

                for step in sample_steps:
                    with st.expander(f"Step {step.index}: {step.title}"):
                        st.write(f"**Task:** {step.description}")
                        st.success(f"**🎓 Educational Features to Build:** {step.teaching_guidance}")

    with tab3:
        st.subheader("Agent Output")

        # Display enriched phases with teaching guidance
        if st.session_state.get("phases"):
            phases = st.session_state.phases

            st.write("**Enriched Project Plan with Educational Feature Guidance:**")

            # Show statistics
            all_steps = [s for p in phases for s in p.steps]
            guided_steps = [s for s in all_steps if s.teaching_guidance]

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Steps", len(all_steps))
            with col2:
                st.metric("With Guidance", len(guided_steps))
            with col3:
                coverage = (len(guided_steps) / max(len(all_steps), 1)) * 100
                st.metric("Coverage", f"{coverage:.0f}%")

            # Display each phase with emphasis on educational features
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

                        if step.teaching_guidance:
                            st.success(f"🎓 **Educational Features to Build:** {step.teaching_guidance}")
                        else:
                            st.warning("No teaching guidance for this step")

                        if step.dependencies:
                            deps = ", ".join(str(d) for d in step.dependencies)
                            st.caption(f"📌 Prerequisites: Steps {deps}")

                        st.markdown("---")

            # Show educational strategy
            st.markdown("---")
            st.write("**Educational Strategy:**")
            st.info("""
            Every step now includes guidance for the implementing agent on:
            - What educational features to build (tooltips, examples, docs)
            - How to make the program teach its users
            - What interactive elements to include
            - How to create a learning experience through the UI
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
