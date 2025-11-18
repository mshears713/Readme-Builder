"""
Evaluator Agent detail page.

Displays detailed information about the EvaluatorAgent's execution.
"""

import streamlit as st
from streamlit_ui.utils import display_evaluation_result


def render():
    """Render the Evaluator Agent page."""
    st.title("✅ Evaluator Agent")
    st.markdown("Quality control and validation of the complete project plan")

    st.markdown("---")

    # Agent description
    with st.expander("ℹ️ About This Agent", expanded=False):
        st.markdown("""
        **Purpose:** Validates the quality of the complete project plan using a multi-criteria rubric.

        **What it does:**
        - Evaluates plan against 5 quality criteria
        - Checks for consistency and completeness
        - Identifies critical issues and suggests improvements
        - Approves plan or requests revisions
        - Triggers refinement iterations if needed

        **Evaluation Criteria:**
        1. **Clarity**: Is the plan clear and unambiguous?
        2. **Feasibility**: Can this be built in the estimated time?
        3. **Teaching Value**: Does it provide strong learning outcomes?
        4. **Technical Depth**: Is the technical challenge appropriate?
        5. **Balance**: Are phases and steps evenly distributed?

        **Input:**
        - Complete `ProjectPlan` with all components

        **Output:**
        - `EvaluationResult` object with:
            - `approved`: Boolean (pass/fail)
            - `scores`: Dictionary of RubricScore for each criterion
            - `feedback`: Multi-paragraph assessment
            - `critical_issues`: List of blocking problems
            - `suggestions`: List of improvement recommendations
            - `architecture_notes`: Highlights on structure and pacing
            - `performance_alerts` / `resilience_risks`: Warnings about runtime safety
            - `test_recommendations`: Actionable coverage hints
            - `naming_feedback`: Style critique for phase/step names

        **Model:** Uses LLM with quality assessment rubrics
        """)

    st.markdown("---")

    # Check if agent has completed
    if not st.session_state.get("EvaluatorAgent_completed", False):
        st.info("⏸️ This agent hasn't run yet. Go to Home page to start execution.")
        return

    # Display execution status
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.session_state.get("evaluation_result"):
            if st.session_state.evaluation_result.approved:
                st.success("✅ Plan Approved")
            else:
                st.error("❌ Plan Rejected")
    with col2:
        iterations = st.session_state.get("iterations", 0)
        st.metric("Iterations", iterations)
    with col3:
        if st.session_state.get("agent_logs", {}).get("EvaluatorAgent"):
            log_count = len(st.session_state.agent_logs["EvaluatorAgent"])
            st.info(f"📋 {log_count} log entries")

    st.markdown("---")

    # Display in sections
    tab1, tab2, tab3, tab4 = st.tabs(["📥 Input", "🔄 Processing", "📤 Output", "🔍 Logs"])

    with tab1:
        st.subheader("Input Received")

        # Display complete plan summary
        st.write("**Complete Project Plan:**")

        col1, col2 = st.columns(2)

        with col1:
            if st.session_state.get("project_idea"):
                st.write("**Project Concept:**")
                st.info(st.session_state.project_idea.refined_summary[:200] + "...")

        with col2:
            if st.session_state.get("framework_choice"):
                framework = st.session_state.framework_choice
                st.write("**Technology Stack:**")
                tech_parts = []
                if framework.frontend:
                    tech_parts.append(f"Frontend: {framework.frontend}")
                if framework.backend:
                    tech_parts.append(f"Backend: {framework.backend}")
                if framework.storage:
                    tech_parts.append(f"Storage: {framework.storage}")
                st.info("\n".join(tech_parts))

        if st.session_state.get("project_goals"):
            goals = st.session_state.project_goals
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Learning Goals", len(goals.learning_goals))
            with col2:
                st.metric("Technical Goals", len(goals.technical_goals))

        if st.session_state.get("phases"):
            phases = st.session_state.phases
            total_steps = sum(len(p.steps) for p in phases)
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Phases", len(phases))
            with col2:
                st.metric("Total Steps", total_steps)

    with tab2:
        st.subheader("Agent Processing")

        st.markdown("""
        **Evaluation Process:**

        1. **Rubric Scoring**: Evaluates plan against 5 quality criteria (each scored 0-10)
        2. **Consistency Check**: Validates structural integrity and dependencies
        3. **Completeness Validation**: Ensures all goals are addressed
        4. **Architecture Review**: Summarizes pacing, naming, and distribution notes
        5. **Issue Identification**: Finds critical problems that block approval
        6. **Suggestion Generation**: Provides improvement recommendations and test hints
        7. **Approval Decision**: Approves or rejects based on scoring thresholds
        8. **Iteration Trigger**: Requests refinement if quality is insufficient
        """)

        st.write("**Quality Thresholds:**")

        thresholds = {
            "Clarity": "≥ 7/10",
            "Feasibility": "≥ 7/10",
            "Teaching Value": "≥ 6/10",
            "Technical Depth": "≥ 6/10",
            "Balance": "≥ 6/10"
        }

        for criterion, threshold in thresholds.items():
            st.write(f"- **{criterion}**: {threshold}")

        st.info("""
        **Approval Logic**: Plan must meet or exceed ALL threshold scores.
        If any score is too low, the plan is rejected and suggestions are provided
        for refinement.
        """)

    with tab3:
        st.subheader("Agent Output")

        # Display the evaluation result
        if st.session_state.get("evaluation_result"):
            display_evaluation_result(st.session_state.evaluation_result)

            evaluation = st.session_state.evaluation_result

            # Show detailed score breakdown
            if hasattr(evaluation, 'scores') and evaluation.scores:
                st.markdown("---")
                st.write("**Detailed Score Analysis:**")

                for criterion, score in evaluation.scores.items():
                    criterion_name = str(criterion).split(".")[-1].replace("_", " ").title()
                    score_value = score.score if hasattr(score, 'score') else score

                    # Color based on score
                    if score_value >= 8:
                        status = "🟢 Excellent"
                    elif score_value >= 7:
                        status = "🟡 Good"
                    elif score_value >= 6:
                        status = "🟠 Acceptable"
                    else:
                        status = "🔴 Needs Work"

                    with st.expander(f"{criterion_name}: {score_value}/10 - {status}"):
                        if hasattr(score, 'feedback') and score.feedback:
                            st.write(score.feedback)
                        else:
                            st.write("No detailed feedback available")

            # Show refinement history if iterations > 1
            iterations = st.session_state.get("iterations", 1)
            if iterations > 1:
                st.markdown("---")
                st.write(f"**Refinement History:** {iterations} iterations")
                st.info(f"""
                This plan went through {iterations} refinement cycles before approval.
                Each iteration improved quality based on evaluator feedback.
                """)

            # Overall assessment
            st.markdown("---")
            if evaluation.approved:
                st.success("""
                ✅ **Plan Approved!**

                This project plan meets all quality standards and is ready for
                implementation. The plan is clear, feasible, educationally valuable,
                technically appropriate, and well-balanced.
                """)
            else:
                st.error("""
                ❌ **Plan Needs Revision**

                This plan did not meet quality thresholds and requires refinement.
                Review critical issues and suggestions above.
                """)
        else:
            st.warning("No evaluation data available")

    with tab4:
        st.subheader("Agent Logs")

        # Display agent-specific logs
        if st.session_state.get("agent_logs", {}).get("EvaluatorAgent"):
            logs = st.session_state.agent_logs["EvaluatorAgent"]
            for log in logs:
                st.text(f"[{log['timestamp']}] {log['message']}")
        else:
            st.info("No agent-specific logs available")

        # Show iteration history if available
        iterations = st.session_state.get("iterations", 1)
        if iterations > 1:
            st.markdown("---")
            st.write("**Iteration History:**")
            for i in range(1, iterations + 1):
                if i == iterations:
                    st.success(f"Iteration {i}: ✅ Approved")
                else:
                    st.warning(f"Iteration {i}: 🔄 Refinement needed")
