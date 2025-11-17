"""
Logs and debugging page.

Displays execution logs, error messages, and debugging information.
"""

import streamlit as st
from datetime import datetime


def render():
    """Render the logs and debugging page."""
    st.title("🔍 Logs & Debug Information")
    st.markdown("Execution logs, error messages, and debugging output")

    st.markdown("---")

    # Check if execution has started
    if not st.session_state.get("execution_started", False):
        st.info("No execution data available. Run a pipeline from the Home page to see logs.")
        return

    # Execution summary
    st.subheader("Execution Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.session_state.get("execution_completed"):
            st.success("✅ Completed")
        elif st.session_state.get("execution_error"):
            st.error("❌ Error")
        else:
            st.warning("⏳ Running")

    with col2:
        phase = st.session_state.get("phase", "N/A")
        st.metric("Phase", phase)

    with col3:
        iterations = st.session_state.get("iterations", 0)
        st.metric("Iterations", iterations)

    with col4:
        if st.session_state.get("start_time"):
            start = st.session_state.start_time
            st.metric("Started", start.strftime("%H:%M:%S"))

    # Timing information
    if st.session_state.get("start_time"):
        st.markdown("---")
        st.write("**Timing:**")

        start_time = st.session_state.start_time
        end_time = st.session_state.get("end_time", datetime.now())

        # Ensure both times are valid before calculating elapsed time
        if start_time is not None and end_time is not None:
            elapsed = end_time - start_time
        else:
            elapsed = None

        col1, col2, col3 = st.columns(3)
        with col1:
            if start_time:
                st.write(f"**Start:** {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                st.write("**Start:** N/A")
        with col2:
            if st.session_state.get("end_time") and end_time:
                st.write(f"**End:** {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                st.write("**End:** In progress...")
        with col3:
            if elapsed:
                minutes = int(elapsed.total_seconds() // 60)
                seconds = int(elapsed.total_seconds() % 60)
                st.write(f"**Duration:** {minutes}m {seconds}s")
            else:
                st.write("**Duration:** N/A")

    st.markdown("---")

    # Display in tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Execution Logs",
        "🤖 Agent Logs",
        "💬 Captured Output",
        "❌ Errors",
        "📊 Debug Info"
    ])

    with tab1:
        st.subheader("Execution Logs")

        # Filter controls
        col1, col2 = st.columns([2, 1])
        with col1:
            log_filter = st.selectbox(
                "Filter by level:",
                options=["ALL", "DEBUG", "INFO", "WARNING", "ERROR"],
                index=0
            )
        with col2:
            show_timestamps = st.checkbox("Show timestamps", value=True)

        # Display logs
        if st.session_state.get("execution_logs"):
            logs = st.session_state.execution_logs

            # Filter logs
            if log_filter != "ALL":
                logs = [log for log in logs if log["level"] == log_filter]

            if logs:
                for log in logs:
                    level = log["level"]
                    timestamp = log["timestamp"]
                    message = log["message"]

                    # Color based on level
                    if level == "ERROR":
                        log_color = "🔴"
                    elif level == "WARNING":
                        log_color = "🟡"
                    elif level == "INFO":
                        log_color = "🔵"
                    else:
                        log_color = "⚪"

                    if show_timestamps:
                        st.text(f"{log_color} [{timestamp}] [{level}] {message}")
                    else:
                        st.text(f"{log_color} [{level}] {message}")
            else:
                st.info(f"No logs at level: {log_filter}")
        else:
            st.info("No execution logs available")

        # Export logs
        if st.session_state.get("execution_logs"):
            st.markdown("---")
            log_text = "\n".join([
                f"[{log['timestamp']}] [{log['level']}] {log['message']}"
                for log in st.session_state.execution_logs
            ])
            st.download_button(
                label="📥 Download Logs",
                data=log_text,
                file_name=f"project_forge_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

    with tab2:
        st.subheader("Agent-Specific Logs")

        # Display logs for each agent
        if st.session_state.get("agent_logs"):
            agent_logs = st.session_state.agent_logs

            if agent_logs:
                # Agent selector
                agents_with_logs = list(agent_logs.keys())
                selected_agent = st.selectbox(
                    "Select agent:",
                    options=agents_with_logs
                )

                if selected_agent:
                    logs = agent_logs[selected_agent]

                    st.write(f"**{selected_agent} Logs:** ({len(logs)} entries)")

                    for log in logs:
                        timestamp = log["timestamp"]
                        message = log["message"]
                        st.text(f"[{timestamp}] {message}")
            else:
                st.info("No agent-specific logs available")
        else:
            st.info("No agent-specific logs available")

    with tab3:
        st.subheader("Captured stdout/stderr")

        # Show captured output from pipeline execution
        sub_tab1, sub_tab2 = st.tabs(["stdout", "stderr"])

        with sub_tab1:
            if st.session_state.get("captured_stdout"):
                stdout = st.session_state.captured_stdout
                st.write(f"**Captured stdout** ({len(stdout)} characters)")
                st.code(stdout, language="text")
            else:
                st.info("No stdout captured")

        with sub_tab2:
            if st.session_state.get("captured_stderr"):
                stderr = st.session_state.captured_stderr
                st.write(f"**Captured stderr** ({len(stderr)} characters)")
                st.code(stderr, language="text")
            else:
                st.info("No stderr captured")

    with tab4:
        st.subheader("Error Information")

        # Display error details
        if st.session_state.get("execution_error"):
            error = st.session_state.execution_error

            st.error("**Execution Error:**")
            st.code(error, language="text")

            # Show error logs
            error_logs = [
                log for log in st.session_state.get("execution_logs", [])
                if log["level"] == "ERROR"
            ]

            if error_logs:
                st.write("**Error Logs:**")
                for log in error_logs:
                    st.text(f"[{log['timestamp']}] {log['message']}")

            # Troubleshooting tips
            st.markdown("---")
            st.write("**Troubleshooting Tips:**")
            st.info("""
            1. Check the error message for specific issues
            2. Review agent logs for the failing agent
            3. Verify API keys and environment variables
            4. Check input parameters (skill level, project idea)
            5. Review captured stdout/stderr for additional context
            6. Try reducing max_iterations if timeout issues occur
            """)
        else:
            st.success("✅ No errors encountered")

    with tab5:
        st.subheader("Debug Information")

        # Display session state for debugging
        st.write("**Session State Variables:**")

        debug_vars = {
            "execution_started": st.session_state.get("execution_started"),
            "execution_completed": st.session_state.get("execution_completed"),
            "execution_error": st.session_state.get("execution_error"),
            "current_agent": st.session_state.get("current_agent"),
            "progress_percent": st.session_state.get("progress_percent"),
            "raw_idea": st.session_state.get("raw_idea", "")[:100] + "..." if st.session_state.get("raw_idea") else None,
            "skill_level": st.session_state.get("skill_level"),
            "phase": st.session_state.get("phase"),
            "max_iterations": st.session_state.get("max_iterations"),
            "iterations": st.session_state.get("iterations"),
        }

        for key, value in debug_vars.items():
            col1, col2 = st.columns([1, 2])
            with col1:
                st.write(f"**{key}:**")
            with col2:
                st.write(str(value))

        # Agent completion status
        st.markdown("---")
        st.write("**Agent Completion Status:**")

        agents = [
            "ConceptExpander",
            "GoalsAnalyzer",
            "FrameworkSelector",
            "PhaseDesigner",
            "TeacherAgent",
            "EvaluatorAgent",
            "PRDWriter"
        ]

        for agent in agents:
            completed = st.session_state.get(f"{agent}_completed", False)
            status = "✅" if completed else "⏸️"
            st.write(f"{status} {agent}")

        # Output presence check
        st.markdown("---")
        st.write("**Output Data Availability:**")

        outputs = {
            "project_idea": "ProjectIdea",
            "project_goals": "ProjectGoals",
            "framework_choice": "FrameworkChoice",
            "phases": "Phases",
            "evaluation_result": "EvaluationResult",
            "readme_content": "README Content",
            "project_name": "Project Name"
        }

        for key, label in outputs.items():
            value = st.session_state.get(key)
            status = "✅" if value else "❌"
            st.write(f"{status} {label}")

        # Export debug info
        st.markdown("---")
        if st.button("📥 Export Debug Snapshot"):
            debug_snapshot = {
                "timestamp": datetime.now().isoformat(),
                "session_state": {
                    k: str(v) for k, v in debug_vars.items()
                },
                "agent_completion": {
                    agent: st.session_state.get(f"{agent}_completed", False)
                    for agent in agents
                },
                "output_availability": {
                    label: bool(st.session_state.get(key))
                    for key, label in outputs.items()
                }
            }

            import json
            snapshot_json = json.dumps(debug_snapshot, indent=2)

            st.download_button(
                label="Download Debug Snapshot",
                data=snapshot_json,
                file_name=f"debug_snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
