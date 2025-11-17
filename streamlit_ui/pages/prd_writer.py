"""
PRD Writer Agent detail page.

Displays detailed information about the PRDWriterAgent's execution.
"""

import streamlit as st
from streamlit_ui.utils import display_readme_preview


def render():
    """Render the PRD Writer agent page."""
    st.title("📄 PRD Writer Agent")
    st.markdown("Generates comprehensive README/PRD documents in markdown format")

    st.markdown("---")

    # Agent description
    with st.expander("ℹ️ About This Agent", expanded=False):
        st.markdown("""
        **Purpose:** Converts the structured ProjectPlan into a comprehensive, narrative README/PRD document.

        **What it does:**
        - Generates a professional README.md file
        - Includes project overview, learning objectives, and tech stack
        - Documents all 5 phases with detailed step descriptions
        - Adds teaching notes and learning context
        - Formats content for readability and clarity
        - Creates a document ready for code LLM consumption

        **Input:**
        - Complete `ProjectPlan` (validated and approved by Evaluator)
        - `EvaluationResult` for quality context

        **Output:**
        - `readme_content`: Full markdown document as string
        - `project_name`: Generated project name for the file

        **Document Sections:**
        1. Project title and overview
        2. Learning objectives
        3. Technical goals
        4. Technology stack
        5. Project structure (5 phases with all steps)
        6. Teaching notes and learning guidance
        7. Next steps and deployment notes

        **Model:** Uses LLM with technical writing expertise
        """)

    st.markdown("---")

    # Check if agent has completed
    if not st.session_state.get("PRDWriter_completed", False):
        st.info("⏸️ This agent hasn't run yet. Run Phase 4 to generate README.")
        return

    # Display execution status
    col1, col2, col3 = st.columns(3)
    with col1:
        st.success("✅ README Generated")
    with col2:
        if st.session_state.get("readme_content"):
            char_count = len(st.session_state.readme_content)
            st.metric("Characters", f"{char_count:,}")
    with col3:
        if st.session_state.get("readme_content"):
            line_count = st.session_state.readme_content.count('\n') + 1
            st.metric("Lines", line_count)

    st.markdown("---")

    # Display in sections
    tab1, tab2, tab3, tab4 = st.tabs(["📥 Input", "🔄 Processing", "📤 Output", "🔍 Logs"])

    with tab1:
        st.subheader("Input Received")

        # Display project plan summary
        st.write("**Complete Approved Project Plan:**")

        if st.session_state.get("project_idea"):
            st.write("**Project:**")
            st.info(st.session_state.project_idea.refined_summary)

        col1, col2 = st.columns(2)
        with col1:
            if st.session_state.get("project_goals"):
                goals = st.session_state.project_goals
                st.metric("Learning Goals", len(goals.learning_goals))
                st.metric("Technical Goals", len(goals.technical_goals))

        with col2:
            if st.session_state.get("phases"):
                phases = st.session_state.phases
                total_steps = sum(len(p.steps) for p in phases)
                st.metric("Phases", len(phases))
                st.metric("Total Steps", total_steps)

        if st.session_state.get("evaluation_result"):
            evaluation = st.session_state.evaluation_result
            if evaluation.approved:
                st.success("✅ Plan was approved by Evaluator")
            else:
                st.warning("⚠️ Plan had issues but was used anyway")

    with tab2:
        st.subheader("Agent Processing")

        st.markdown("""
        **README Generation Process:**

        1. **Extract Metadata**: Gets project name, description, goals
        2. **Format Overview**: Creates introduction and context sections
        3. **Document Goals**: Writes learning and technical objectives
        4. **Describe Tech Stack**: Lists all frameworks and libraries
        5. **Structure Phases**: Organizes 5 phases with all steps
        6. **Add Teaching Context**: Includes pedagogical annotations
        7. **Format Markdown**: Applies proper headings, lists, and formatting
        8. **Generate File Name**: Creates appropriate project name
        9. **Validate Output**: Ensures markdown is valid and complete
        """)

        st.write("**README Structure:**")

        structure = [
            "# Project Title",
            "## Overview",
            "## What You'll Learn",
            "## What You'll Build",
            "## Technology Stack",
            "## Project Structure",
            "### Phase 1: [Name]",
            "#### Step 1: [Title]",
            "...",
            "### Phase 5: [Name]",
            "## Teaching Notes",
            "## Next Steps"
        ]

        for item in structure:
            indent = "  " * (item.count("#") - 1)
            st.text(f"{indent}{item}")

        st.info("""
        The generated README follows a consistent structure that makes it:
        - **Clear** for human readers to understand the project
        - **Actionable** for code LLMs to implement
        - **Educational** with learning context throughout
        - **Complete** with all necessary implementation details
        """)

    with tab3:
        st.subheader("Agent Output")

        # Display the README content
        if st.session_state.get("readme_content"):
            # Show README preview with all features
            display_readme_preview(st.session_state.readme_content, max_lines=100)

            # Show README statistics
            st.markdown("---")
            st.write("**README Statistics:**")

            readme = st.session_state.readme_content
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                char_count = len(readme)
                st.metric("Characters", f"{char_count:,}")

            with col2:
                word_count = len(readme.split())
                st.metric("Words", f"{word_count:,}")

            with col3:
                line_count = readme.count('\n') + 1
                st.metric("Lines", line_count)

            with col4:
                heading_count = readme.count('\n#')
                st.metric("Sections", heading_count)

            # Project name
            if st.session_state.get("project_name"):
                st.markdown("---")
                st.write("**Generated Project Name:**")
                st.code(st.session_state.project_name, language="text")

            # Download options
            st.markdown("---")
            st.write("**Export Options:**")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.download_button(
                    label="📥 Download README.md",
                    data=readme,
                    file_name=f"{st.session_state.get('project_name', 'project')}_README.md",
                    mime="text/markdown",
                    use_container_width=True
                )

            with col2:
                # Copy to clipboard (via text area)
                if st.button("📋 Show Copyable Text", use_container_width=True):
                    st.text_area(
                        "Copy this text:",
                        value=readme,
                        height=400
                    )

            with col3:
                # Show raw markdown
                if st.button("🔍 Show Raw Markdown", use_container_width=True):
                    st.code(readme, language="markdown")

        else:
            st.warning("No README content available. Run Phase 4 to generate.")

    with tab4:
        st.subheader("Agent Logs")

        # Display agent-specific logs
        if st.session_state.get("agent_logs", {}).get("PRDWriter"):
            logs = st.session_state.agent_logs["PRDWriter"]
            for log in logs:
                st.text(f"[{log['timestamp']}] {log['message']}")
        else:
            st.info("No agent-specific logs available")
