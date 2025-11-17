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
    reset_execution_state, add_log, update_progress,
    mark_agent_completed, get_elapsed_time, CaptureOutput,
    display_project_idea, display_project_goals,
    display_framework_choice, display_phases,
    display_evaluation_result, display_readme_preview
)


def run_pipeline(raw_idea: str, skill_level: str, phase: int, max_iterations: int, verbose: bool):
    """
    Execute the Project Forge pipeline and update session state with results.

    Args:
        raw_idea: The user's project idea
        skill_level: Skill level (beginner/intermediate/advanced)
        phase: Which phase to run (2, 3, or 4)
        max_iterations: Maximum refinement iterations
        verbose: Whether to show verbose output
    """
    try:
        # Import orchestration functions
        from project_forge.src.orchestration.crew_config import (
            create_planning_crew,
            create_full_plan_crew,
            create_complete_pipeline
        )

        st.session_state.execution_started = True
        st.session_state.start_time = datetime.now()
        add_log(f"Starting Phase {phase} pipeline for: {raw_idea[:50]}...", "INFO")

        # Capture output
        with CaptureOutput() as capture:
            if phase == 2:
                # Phase 2: Planning only (ConceptExpander, GoalsAnalyzer, FrameworkSelector)
                add_log("Running Phase 2: Planning Crew", "INFO")
                update_progress("ConceptExpander", 10)

                result = create_planning_crew(
                    raw_idea=raw_idea,
                    skill_level=skill_level,
                    verbose=verbose
                )

                # Store results
                st.session_state.planning_result = result
                st.session_state.project_idea = result.project_idea
                st.session_state.project_goals = result.project_goals
                st.session_state.framework_choice = result.framework_choice
                st.session_state.clarity_score = result.clarity_score

                # Mark agents completed
                mark_agent_completed("ConceptExpander")
                update_progress("GoalsAnalyzer", 40)
                mark_agent_completed("GoalsAnalyzer")
                update_progress("FrameworkSelector", 70)
                mark_agent_completed("FrameworkSelector")
                update_progress("FrameworkSelector", 100)

            elif phase == 3:
                # Phase 3: Full plan with teaching (adds PhaseDesigner, TeacherAgent, EvaluatorAgent)
                add_log("Running Phase 3: Full Plan Crew", "INFO")
                update_progress("ConceptExpander", 5)

                result = create_full_plan_crew(
                    raw_idea=raw_idea,
                    skill_level=skill_level,
                    verbose=verbose,
                    max_iterations=max_iterations
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
                update_progress("GoalsAnalyzer", 20)
                mark_agent_completed("GoalsAnalyzer")
                update_progress("FrameworkSelector", 35)
                mark_agent_completed("FrameworkSelector")
                update_progress("PhaseDesigner", 50)
                mark_agent_completed("PhaseDesigner")
                update_progress("TeacherAgent", 70)
                mark_agent_completed("TeacherAgent")
                update_progress("EvaluatorAgent", 90)
                mark_agent_completed("EvaluatorAgent")
                update_progress("EvaluatorAgent", 100)

            elif phase == 4:
                # Phase 4: Complete pipeline with README (all 7 agents)
                add_log("Running Phase 4: Complete Pipeline", "INFO")
                update_progress("ConceptExpander", 5)

                result = create_complete_pipeline(
                    raw_idea=raw_idea,
                    skill_level=skill_level,
                    verbose=verbose,
                    max_iterations=max_iterations
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
                update_progress("GoalsAnalyzer", 15)
                mark_agent_completed("GoalsAnalyzer")
                update_progress("FrameworkSelector", 30)
                mark_agent_completed("FrameworkSelector")
                update_progress("PhaseDesigner", 45)
                mark_agent_completed("PhaseDesigner")
                update_progress("TeacherAgent", 60)
                mark_agent_completed("TeacherAgent")
                update_progress("EvaluatorAgent", 75)
                mark_agent_completed("EvaluatorAgent")
                update_progress("PRDWriter", 90)
                mark_agent_completed("PRDWriter")
                update_progress("PRDWriter", 100)

        # Store captured output
        st.session_state.captured_stdout = capture.get_stdout()
        st.session_state.captured_stderr = capture.get_stderr()

        # Mark completion
        st.session_state.execution_completed = True
        st.session_state.end_time = datetime.now()
        add_log("Pipeline execution completed successfully", "INFO")

    except Exception as e:
        st.session_state.execution_error = str(e)
        st.session_state.end_time = datetime.now()
        error_trace = traceback.format_exc()
        add_log(f"Pipeline execution failed: {str(e)}", "ERROR")
        add_log(f"Traceback: {error_trace}", "ERROR")
        st.error(f"Error: {str(e)}")
        st.error("See Logs & Debug page for details")


def render():
    """Render the home page."""
    st.markdown('<h1 class="main-header">🔨 Project Forge</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Multi-Agent README Generator</p>', unsafe_allow_html=True)

    st.markdown("---")

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
            reset_execution_state()
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

                # Run the pipeline
                with st.spinner("Running multi-agent pipeline... This may take 2-5 minutes."):
                    run_pipeline(raw_idea, skill_level, phase, max_iterations, verbose)
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
                reset_execution_state()
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
            reset_execution_state()
            st.rerun()
