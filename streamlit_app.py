"""
Project Forge - Streamlit UI
Multi-Agent README Generator with Interactive Visualization

This Streamlit application provides an interactive interface for the Project Forge
multi-agent system. Users can input project ideas, track agent execution in real-time,
and explore detailed outputs from each of the 7 agents in the pipeline.
"""

import streamlit as st
from streamlit_ui.utils import initialize_session_state
from streamlit_ui.pages import home, logs

# Page configuration
st.set_page_config(
    page_title="Project Forge - Multi-Agent README Generator",
    page_icon="🔨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .agent-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .status-running {
        color: #ff9800;
    }
    .status-completed {
        color: #4caf50;
    }
    .status-error {
        color: #f44336;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
initialize_session_state()

# Sidebar Navigation
st.sidebar.title("🔨 Project Forge")
st.sidebar.markdown("---")

# Navigation menu
page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📝 Concept Expander",
        "🎯 Goals Analyzer",
        "🔧 Framework Selector",
        "📋 Phase Designer",
        "👨‍🏫 Teacher Agent",
        "✅ Evaluator Agent",
        "📄 PRD Writer",
        "🔍 Logs & Debug"
    ]
)

# Display agent execution status in sidebar
if st.session_state.get("execution_started", False):
    st.sidebar.markdown("---")
    st.sidebar.subheader("Execution Status")

    current_agent = st.session_state.get("current_agent", "Not started")
    progress = st.session_state.get("progress_percent", 0)

    st.sidebar.progress(progress / 100.0)
    st.sidebar.write(f"**Current Agent:** {current_agent}")
    st.sidebar.write(f"**Progress:** {progress}%")

    if st.session_state.get("execution_completed", False):
        st.sidebar.success("✅ Execution Complete!")
    elif st.session_state.get("execution_error", None):
        st.sidebar.error("❌ Error occurred")

# Agent completion status
if st.session_state.get("execution_started", False):
    st.sidebar.markdown("---")
    st.sidebar.subheader("Agent Progress")

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
        if st.session_state.get(f"{agent}_completed", False):
            st.sidebar.success(f"✅ {agent}")
        elif st.session_state.get("current_agent") == agent:
            st.sidebar.warning(f"⏳ {agent}")
        else:
            st.sidebar.info(f"⏸️ {agent}")

# Main content area - Route to appropriate page
if page == "🏠 Home":
    home.render()
elif page == "📝 Concept Expander":
    from streamlit_ui.pages import concept_expander
    concept_expander.render()
elif page == "🎯 Goals Analyzer":
    from streamlit_ui.pages import goals_analyzer
    goals_analyzer.render()
elif page == "🔧 Framework Selector":
    from streamlit_ui.pages import framework_selector
    framework_selector.render()
elif page == "📋 Phase Designer":
    from streamlit_ui.pages import phase_designer
    phase_designer.render()
elif page == "👨‍🏫 Teacher Agent":
    from streamlit_ui.pages import teacher_agent
    teacher_agent.render()
elif page == "✅ Evaluator Agent":
    from streamlit_ui.pages import evaluator_agent
    evaluator_agent.render()
elif page == "📄 PRD Writer":
    from streamlit_ui.pages import prd_writer
    prd_writer.render()
elif page == "🔍 Logs & Debug":
    logs.render()

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.8rem;'>
        <p>Project Forge v1.0</p>
        <p>Multi-Agent README Generator</p>
        <p>Powered by CrewAI & OpenAI</p>
    </div>
    """,
    unsafe_allow_html=True
)
