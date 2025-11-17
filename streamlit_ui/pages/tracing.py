"""
Tracing and Observability page.

Provides information about setting up and using tracing tools like LangSmith
to debug and monitor the multi-agent pipeline.
"""

import streamlit as st
import os


def render():
    """Render the tracing and observability page."""
    st.title("🔍 Tracing & Observability")
    st.markdown("Debug and monitor your multi-agent pipeline with tracing tools")

    st.markdown("---")

    # Check tracing configuration
    st.subheader("Current Configuration")

    langchain_enabled = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
    langchain_api_key = os.getenv("LANGCHAIN_API_KEY", "")
    langchain_project = os.getenv("LANGCHAIN_PROJECT", "project-forge")

    langfuse_public_key = os.getenv("LANGFUSE_PUBLIC_KEY", "")
    langfuse_secret_key = os.getenv("LANGFUSE_SECRET_KEY", "")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**LangSmith Status:**")
        if langchain_enabled and langchain_api_key:
            st.success("✅ Enabled")
            st.info(f"**Project:** {langchain_project}")
        elif langchain_api_key:
            st.warning("⚠️ API key set but tracing not enabled")
        else:
            st.error("❌ Not configured")

    with col2:
        st.write("**LangFuse Status:**")
        if langfuse_public_key and langfuse_secret_key:
            st.success("✅ Configured")
        else:
            st.error("❌ Not configured")

    st.markdown("---")

    # Setup instructions
    st.subheader("Setup Instructions")

    tab1, tab2, tab3 = st.tabs([
        "🔵 LangSmith (Recommended)",
        "🟢 LangFuse (Open Source)",
        "📊 Viewing Traces"
    ])

    with tab1:
        st.markdown("""
        ### LangSmith Setup

        LangSmith is a powerful observability platform for LLM applications from LangChain.

        **Why use LangSmith?**
        - 📊 Visualize agent execution flow
        - 🐛 Debug stuck or failing agents
        - ⏱️ Track latency and token usage
        - 🔍 Inspect LLM inputs and outputs
        - 📈 Monitor performance over time

        **Setup Steps:**

        1. **Sign up for LangSmith** (free tier available)
           - Visit: [https://smith.langchain.com](https://smith.langchain.com)
           - Create an account

        2. **Get your API key**
           - Go to: [https://smith.langchain.com/settings](https://smith.langchain.com/settings)
           - Create a new API key
           - Copy the key

        3. **Configure environment variables**
           - Open your `.env` file in the project root
           - Add the following lines:
           ```bash
           LANGCHAIN_TRACING_V2=true
           LANGCHAIN_API_KEY=your_api_key_here
           LANGCHAIN_PROJECT=project-forge
           LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
           ```

        4. **Restart the application**
           - Stop the Streamlit server (Ctrl+C)
           - Restart: `streamlit run streamlit_app.py`

        5. **Run a pipeline**
           - Go to the Home page and run any pipeline
           - Traces will appear in your LangSmith dashboard

        6. **View traces**
           - Visit: [https://smith.langchain.com](https://smith.langchain.com)
           - Navigate to your project: "project-forge"
           - Browse traces by time, agent, or status
        """)

        st.info("""
        **Pro Tip:** Create different projects for different environments:
        - `project-forge-dev` for development
        - `project-forge-prod` for production
        - `project-forge-testing` for experiments
        """)

    with tab2:
        st.markdown("""
        ### LangFuse Setup (Open Source Alternative)

        LangFuse is an open-source observability platform you can self-host or use their cloud.

        **Why use LangFuse?**
        - 🆓 Open source and self-hostable
        - 📊 Similar features to LangSmith
        - 🔒 Keep data on your own infrastructure
        - 💰 Free for unlimited use (self-hosted)

        **Setup Steps:**

        1. **Choose hosting option**

           **Option A: Cloud (Easiest)**
           - Visit: [https://cloud.langfuse.com](https://cloud.langfuse.com)
           - Sign up for free account

           **Option B: Self-host (Most control)**
           - Follow guide: [https://langfuse.com/docs/deployment/self-host](https://langfuse.com/docs/deployment/self-host)
           - Deploy using Docker, Vercel, or Railway

        2. **Get your API keys**
           - In LangFuse dashboard, go to Settings → API Keys
           - Create a new key pair (public + secret)
           - Copy both keys

        3. **Configure environment variables**
           - Open your `.env` file
           - Add:
           ```bash
           LANGFUSE_PUBLIC_KEY=pk-lf-...
           LANGFUSE_SECRET_KEY=sk-lf-...
           LANGFUSE_HOST=https://cloud.langfuse.com  # or your self-hosted URL
           ```

        4. **Install LangFuse SDK** (if not already installed)
           ```bash
           pip install langfuse
           ```

        5. **Restart and run**
           - Restart the Streamlit app
           - Run a pipeline
           - View traces in LangFuse dashboard
        """)

        st.warning("""
        **Note:** LangFuse integration requires additional code changes.
        See the project documentation for full integration guide.
        """)

    with tab3:
        st.markdown("""
        ### Viewing and Using Traces

        Once tracing is enabled, you can debug issues like the PRD writer getting stuck.

        **What to look for:**

        1. **Stuck Agents**
           - Look for traces that haven't completed
           - Check if there's a long-running LLM call
           - Inspect the last prompt sent to the LLM

        2. **Error Patterns**
           - Find traces with error status
           - Look at error messages and stack traces
           - Compare failed traces to successful ones

        3. **Performance Issues**
           - Sort traces by duration
           - Identify slow agents or tasks
           - Check token usage for expensive calls

        4. **Agent Behavior**
           - See the exact prompts sent to each agent
           - View LLM responses before parsing
           - Understand decision-making flow

        **Example: Debugging PRD Writer Issues**

        If the PRD Writer gets stuck:
        1. Go to your tracing dashboard
        2. Filter for "PRDWriter" or recent traces
        3. Find the stuck/failed trace
        4. Look for:
           - Last successful operation before hang
           - Any error messages in sub-traces
           - Token counts (may indicate prompt too large)
           - API latency (may indicate timeout)

        **Common Issues and Solutions:**

        | Issue | What to Check in Traces | Solution |
        |-------|------------------------|----------|
        | Agent stuck | Last operation timestamp | Add timeout handling |
        | Empty output | LLM response content | Improve prompt or check API |
        | Parsing errors | Raw LLM output format | Fix parsing logic |
        | Slow execution | Total tokens, API calls | Reduce prompt size or iterations |
        """)

        if langchain_enabled and langchain_api_key:
            st.success("""
            ✅ LangSmith is configured!

            **Quick Links:**
            - Dashboard: [https://smith.langchain.com](https://smith.langchain.com)
            - Your Project: [https://smith.langchain.com/projects](https://smith.langchain.com/projects)
            - Documentation: [https://docs.smith.langchain.com](https://docs.smith.langchain.com)
            """)

    st.markdown("---")

    # Troubleshooting section
    st.subheader("Troubleshooting")

    with st.expander("🔧 Common Issues"):
        st.markdown("""
        **Traces not appearing?**
        1. Check environment variables are set correctly
        2. Restart the Streamlit application
        3. Verify API key is valid
        4. Check network connectivity to tracing service

        **"API key invalid" error?**
        1. Regenerate API key in dashboard
        2. Update `.env` file
        3. Restart application

        **Self-hosted LangFuse not working?**
        1. Verify LANGFUSE_HOST URL is correct
        2. Check firewall/network rules
        3. Ensure LangFuse server is running
        4. Check server logs for errors

        **Still having issues?**
        - Check the logs in the "Logs & Debug" page
        - Review captured stderr for tracing errors
        - Consult LangSmith/LangFuse documentation
        - Open an issue on the Project Forge GitHub
        """)

    with st.expander("📚 Additional Resources"):
        st.markdown("""
        **LangSmith:**
        - Documentation: [https://docs.smith.langchain.com](https://docs.smith.langchain.com)
        - Blog: [https://blog.langchain.dev](https://blog.langchain.dev)
        - Discord: [https://discord.gg/langchain](https://discord.gg/langchain)

        **LangFuse:**
        - Documentation: [https://langfuse.com/docs](https://langfuse.com/docs)
        - GitHub: [https://github.com/langfuse/langfuse](https://github.com/langfuse/langfuse)
        - Discord: [https://discord.gg/langfuse](https://discord.gg/langfuse)

        **General LLM Observability:**
        - OpenAI Cookbook: [Observability](https://cookbook.openai.com/examples/observability)
        - CrewAI Documentation: [Observability](https://docs.crewai.com)
        """)

    st.markdown("---")

    # Quick actions
    st.subheader("Quick Actions")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📋 Copy Example .env", use_container_width=True):
            example_env = """# Tracing Configuration
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_api_key_here
LANGCHAIN_PROJECT=project-forge
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com"""
            st.code(example_env, language="bash")

    with col2:
        if st.button("🔍 Check Configuration", use_container_width=True):
            st.write("**Environment Variables:**")
            env_vars = {
                "LANGCHAIN_TRACING_V2": os.getenv("LANGCHAIN_TRACING_V2", "Not set"),
                "LANGCHAIN_API_KEY": "Set" if os.getenv("LANGCHAIN_API_KEY") else "Not set",
                "LANGCHAIN_PROJECT": os.getenv("LANGCHAIN_PROJECT", "Not set"),
                "LANGFUSE_PUBLIC_KEY": "Set" if os.getenv("LANGFUSE_PUBLIC_KEY") else "Not set",
                "LANGFUSE_SECRET_KEY": "Set" if os.getenv("LANGFUSE_SECRET_KEY") else "Not set",
            }
            for key, value in env_vars.items():
                st.text(f"{key}: {value}")

    with col3:
        if st.button("🌐 Open LangSmith", use_container_width=True):
            st.markdown("[Open LangSmith Dashboard →](https://smith.langchain.com)")
