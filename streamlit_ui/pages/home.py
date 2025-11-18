"""
Home page for Project Forge Streamlit UI.

This page provides the main interface for users to:
- Input their project idea
- Configure execution parameters
- Start the multi-agent pipeline
- View execution progress and results
"""

import streamlit as st
from datetime import datetime
import traceback
from streamlit_ui.utils import (
    reset_execution_state,
    add_log,
    update_progress,
    mark_agent_completed,
    get_elapsed_time,
    CaptureOutput,
    display_project_idea,
    display_project_goals,
    display_framework_choice,
    display_phases,
    display_evaluation_result,
    display_readme_preview,
    prepare_new_run_state,
    cleanup_asyncio_tasks,
)


def run_pipeline_with_ui_updates(raw_idea: str, skill_level: str, phase: int, max_iterations: int, verbose: bool,
                                  status_container, progress_bar, agent_display, time_display):
    """
    Execute the Project Forge pipeline with real-time UI updates.

    Args:
        raw_idea: The user's project idea
        skill_level: Skill level (beginner/intermediate/advanced)
        phase: Which phase to run (2, 3, or 4)
        max_iterations: Maximum refinement iterations
        verbose: Whether to show verbose output
        status_container: Streamlit container for status messages
        progress_bar: Streamlit progress bar
        agent_display: Streamlit container for current agent display
        time_display: Streamlit container for elapsed time display
    """
    try:
        # Import orchestration functions
        from project_forge.src.orchestration.crew_config import (
            create_planning_crew,
            create_full_plan_crew,
            create_complete_pipeline
        )

        st.session_state.start_time = st.session_state.start_time or datetime.now()
        add_log(f"Starting Phase {phase} pipeline for: {raw_idea[:50]}...", "INFO")

        def update_ui():
            """Helper to update UI elements during execution."""
            agent_display.info(f"Current Agent: **{st.session_state.get('current_agent', 'Processing...')}**")
            progress_bar.progress(st.session_state.get("progress_percent", 0) / 100.0)
            elapsed = get_elapsed_time()
            if elapsed:
                time_display.write(f"⏱️ Elapsed Time: {elapsed}")

        def progress_callback(agent_name: str, progress: int, message: str):
            """Callback function for backend to report progress."""
            update_progress(agent_name, progress)
            update_ui()
            status_container.write(message)

        # Capture output
        with CaptureOutput() as capture:
            if phase == 2:
                # Phase 2: Planning only (ConceptExpander, GoalsAnalyzer, FrameworkSelector)
                add_log("Running Phase 2: Planning Crew", "INFO")
                status_container.write("🔍 **Phase 2: Planning Crew**")

                result = create_planning_crew(
                    raw_idea=raw_idea,
                    skill_level=skill_level,
                    verbose=verbose,
                    progress_callback=progress_callback
                )

                # Store results
                st.session_state.planning_result = result
                st.session_state.project_idea = result.project_idea
                st.session_state.project_goals = result.project_goals
                st.session_state.framework_choice = result.framework_choice
                st.session_state.clarity_score = result.clarity_score

                # Mark agents completed
                mark_agent_completed("ConceptExpander")
                mark_agent_completed("GoalsAnalyzer")
                mark_agent_completed("FrameworkSelector")

            elif phase == 3:
                # Phase 3: Full plan with teaching (adds PhaseDesigner, TeacherAgent, EvaluatorAgent)
                add_log("Running Phase 3: Full Plan Crew", "INFO")
                status_container.write("🔍 **Phase 3: Full Plan Crew**")

                result = create_full_plan_crew(
                    raw_idea=raw_idea,
                    skill_level=skill_level,
                    verbose=verbose,
                    max_iterations=max_iterations,
                    progress_callback=progress_callback
                )

                # Store results
                st.session_state.full_plan_result = result
                st.session_state.project_idea = result.project_plan.idea
                st.session_state.project_goals = result.project_plan.goals
                st.session_state.framework_choice = result.project_plan.framework
                st.session_state.phases = result.project_plan.phases
                st.session_state.evaluation_result = result.evaluation
                st.session_state.iterations = result.iterations

                # Mark agents completed
                mark_agent_completed("ConceptExpander")
                mark_agent_completed("GoalsAnalyzer")
                mark_agent_completed("FrameworkSelector")
                mark_agent_completed("PhaseDesigner")
                mark_agent_completed("TeacherAgent")
                mark_agent_completed("EvaluatorAgent")

            elif phase == 4:
                # Phase 4: Complete pipeline with README (all 7 agents)
                add_log("Running Phase 4: Complete Pipeline", "INFO")
                status_container.write("🔍 **Phase 4: Complete Pipeline**")

                result = create_complete_pipeline(
                    raw_idea=raw_idea,
                    skill_level=skill_level,
                    verbose=verbose,
                    max_iterations=max_iterations,
                    progress_callback=progress_callback
                )

                # Store results
                st.session_state.final_result = result
                st.session_state.project_idea = result.project_plan.idea
                st.session_state.project_goals = result.project_plan.goals
                st.session_state.framework_choice = result.project_plan.framework
                st.session_state.phases = result.project_plan.phases
                st.session_state.evaluation_result = result.evaluation
                st.session_state.readme_content = result.readme_content
                st.session_state.project_name = result.project_name
                st.session_state.iterations = result.iterations

                # Mark all agents completed
                mark_agent_completed("ConceptExpander")
                mark_agent_completed("GoalsAnalyzer")
                mark_agent_completed("FrameworkSelector")
                mark_agent_completed("PhaseDesigner")
                mark_agent_completed("TeacherAgent")
                mark_agent_completed("EvaluatorAgent")
                mark_agent_completed("PRDWriter")

        # Store captured output
        st.session_state.captured_stdout = capture.get_stdout()
        st.session_state.captured_stderr = capture.get_stderr()

        # Mark completion
        st.session_state.execution_completed = True
        st.session_state.end_time = datetime.now()
        add_log("Pipeline execution completed successfully", "INFO")
        status_container.write("---")
        status_container.success("🎉 **Pipeline completed successfully!**")
        update_ui()

    except Exception as e:
        st.session_state.execution_error = str(e)
        st.session_state.end_time = datetime.now()
        st.session_state.execution_completed = True  # Mark as completed even on error
        error_trace = traceback.format_exc()
        add_log(f"Pipeline execution failed: {str(e)}", "ERROR")
        add_log(f"Traceback: {error_trace}", "ERROR")
        status_container.error(f"❌ **Error:** {str(e)}")
        status_container.info("See Logs & Debug page for details")
    finally:
        cancelled = cleanup_asyncio_tasks()
        if cancelled:
            add_log(f"Cleaned up {cancelled} pending asyncio task(s)", "DEBUG")


def run_pipeline(raw_idea: str, skill_level: str, phase: int, max_iterations: int, verbose: bool):
    """
    Legacy wrapper for run_pipeline_with_ui_updates that doesn't require UI containers.
    Used for backwards compatibility or CLI execution.

    Args:
        raw_idea: The user's project idea
        skill_level: Skill level (beginner/intermediate/advanced)
        phase: Which phase to run (2, 3, or 4)
        max_iterations: Maximum refinement iterations
        verbose: Whether to show verbose output
    """
    # Create dummy containers
    class DummyContainer:
        def write(self, text): pass
        def info(self, text): pass
        def success(self, text): pass
        def error(self, text): pass
        def progress(self, value): pass

    dummy = DummyContainer()
    run_pipeline_with_ui_updates(raw_idea, skill_level, phase, max_iterations, verbose,
                                  dummy, dummy, dummy, dummy)


def render():
    """Render the home page."""
    st.markdown('<h1 class="main-header">🔨 Project Forge</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Multi-Agent README Generator</p>', unsafe_allow_html=True)

    st.markdown("---")

    # Check if we should start execution
    if st.session_state.get("execution_should_start", False):
        st.session_state.execution_should_start = False
        prepare_new_run_state()

        # Show loading UI with progress tracking
        st.warning("⏳ Execution in progress... This may take 2-5 minutes.")

        # Create containers for dynamic updates
        agent_container = st.empty()
        progress_bar = st.empty()
        time_container = st.empty()
        status_expander = st.expander("📋 Detailed Progress", expanded=True)

        with status_expander:
            status_container = st.container()

        # Show initial state
        agent_container.info(f"Current Agent: **{st.session_state.get('current_agent', 'Starting...')}**")
        progress_bar.progress(0)
        time_container.write("⏱️ Elapsed Time: 0s")

        # Run the pipeline with progress updates
        raw_idea = st.session_state.raw_idea
        skill_level = st.session_state.skill_level
        phase = st.session_state.phase
        max_iterations = st.session_state.max_iterations
        verbose = st.session_state.verbose

        # Execute the pipeline with UI updates
        run_pipeline_with_ui_updates(
            raw_idea, skill_level, phase, max_iterations, verbose,
            status_container, progress_bar, agent_container, time_container
        )

        # After completion, rerun to show results
        st.rerun()

    # Check if execution is in progress
    if st.session_state.get("execution_started", False) and not st.session_state.get("execution_completed", False):
        st.warning("⏳ Execution in progress... Please wait for completion.")
        st.info(f"Current Agent: **{st.session_state.get('current_agent')}**")
        st.progress(st.session_state.get("progress_percent", 0) / 100.0)
        elapsed = get_elapsed_time()
        if elapsed:
            st.write(f"Elapsed Time: {elapsed}")
        return

    # Input Section
    st.header("📝 Project Idea Input")

    with st.form("project_input_form"):
        # Project idea text area
        raw_idea = st.text_area(
            "Describe your project idea:",
            value=st.session_state.get("raw_idea", ""),
            height=150,
            placeholder="Example: Build a Streamlit app for tracking daily habits with charts and streak tracking...",
            help="Describe what you want to build. Be as specific or general as you like - the agents will help refine it!"
        )

        # Configuration options
        col1, col2, col3 = st.columns(3)

        with col1:
            skill_level = st.selectbox(
                "Skill Level",
                options=["beginner", "intermediate", "advanced"],
                index=1,
                help="Your programming experience level. This affects framework recommendations and complexity."
            )

        with col2:
            phase = st.selectbox(
                "Pipeline Phase",
                options=[2, 3, 4],
                index=2,
                format_func=lambda x: {
                    2: "Phase 2: Planning (3 agents)",
                    3: "Phase 3: Full Plan (6 agents)",
                    4: "Phase 4: Complete (7 agents + README)"
                }[x],
                help="Which phase of the pipeline to execute. Phase 4 runs all agents and generates README."
            )

        with col3:
            max_iterations = st.number_input(
                "Max Iterations",
                min_value=1,
                max_value=5,
                value=2,
                help="Maximum refinement iterations for evaluation loop."
            )

        # Advanced options
        with st.expander("Advanced Options"):
            verbose = st.checkbox(
                "Verbose Output",
                value=True,
                help="Show detailed agent execution logs"
            )

        # Submit button
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            submit = st.form_submit_button("🚀 Run Pipeline", type="primary", use_container_width=True)
        with col2:
            reset = st.form_submit_button("🔄 Reset", use_container_width=True)

        if reset:
            reset_execution_state(full_reset=True)
            st.rerun()

        if submit:
            if not raw_idea.strip():
                st.error("Please enter a project idea!")
            else:
                # Store input parameters
                st.session_state.raw_idea = raw_idea
                st.session_state.skill_level = skill_level
                st.session_state.phase = phase
                st.session_state.max_iterations = max_iterations
                st.session_state.verbose = verbose

                # Set flag to start execution and reset state
                st.session_state.execution_should_start = True
                st.session_state.execution_started = False
                st.session_state.execution_completed = False
                st.rerun()

    # Results Section
    if st.session_state.get("execution_completed", False):
        st.markdown("---")
        st.header("✅ Execution Results")

        # Display execution summary
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Status", "Completed ✅")
        with col2:
            elapsed = get_elapsed_time()
            st.metric("Duration", elapsed or "N/A")
        with col3:
            st.metric("Iterations", st.session_state.get("iterations", 0))
        with col4:
            st.metric("Phase", st.session_state.get("phase", "N/A"))

        st.markdown("---")

        # Display results in tabs
        tabs = st.tabs([
            "📝 Concept",
            "🎯 Goals",
            "🔧 Framework",
            "📋 Phases",
            "✅ Evaluation",
            "📄 README"
        ])

        with tabs[0]:
            display_project_idea(st.session_state.get("project_idea"))

        with tabs[1]:
            display_project_goals(st.session_state.get("project_goals"))

        with tabs[2]:
            display_framework_choice(st.session_state.get("framework_choice"))

        with tabs[3]:
            display_phases(st.session_state.get("phases"))

        with tabs[4]:
            display_evaluation_result(st.session_state.get("evaluation_result"))

        with tabs[5]:
            if st.session_state.get("readme_content"):
                display_readme_preview(st.session_state.get("readme_content"))
            else:
                st.info("README not generated. Run Phase 4 to generate README.")

        # Action buttons
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("🔄 New Project", use_container_width=True):
                reset_execution_state(full_reset=True)
                st.rerun()
        with col2:
            if st.session_state.get("readme_content"):
                st.download_button(
                    label="📥 Download README",
                    data=st.session_state.readme_content,
                    file_name=f"{st.session_state.get('project_name', 'project')}_README.md",
                    mime="text/markdown",
                    use_container_width=True
                )

    # Display error if any
    if st.session_state.get("execution_error"):
        st.markdown("---")
        st.error("❌ Execution Error")
        st.error(st.session_state.execution_error)
        st.info("Check the **Logs & Debug** page for detailed error information.")

        if st.button("🔄 Try Again"):
            reset_execution_state(full_reset=False)
            st.rerun()
