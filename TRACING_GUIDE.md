# Tracing & Observability Guide

This guide explains how to enable tracing and observability for the Project Forge multi-agent system to help you debug issues and understand agent behavior.

## Quick Start

### Enable LangSmith Tracing (Recommended)

1. **Sign up for LangSmith** (free tier available)
   - Visit: https://smith.langchain.com
   - Create an account

2. **Get your API key**
   - Go to: https://smith.langchain.com/settings
   - Create a new API key
   - Copy the key

3. **Configure environment variables**

   Add to your `.env` file:
   ```bash
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_API_KEY=your_api_key_here
   LANGCHAIN_PROJECT=project-forge
   LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
   ```

4. **Restart the application**
   ```bash
   # Stop the server (Ctrl+C)
   streamlit run streamlit_app.py
   ```

5. **View traces**
   - Run a pipeline from the Home page
   - Visit: https://smith.langchain.com
   - Navigate to your project: "project-forge"
   - Browse traces to see agent execution details

## New Features

### 1. Fixed DateTime Error in Logs

**Issue:** `TypeError: unsupported operand type(s) for -: 'NoneType' and 'datetime.datetime'`

**Fix:** Added proper None checks before datetime operations in `streamlit_ui/pages/logs.py:lines/56-80`

Now the logs page safely handles cases where start_time or end_time are not set.

### 2. PRD Writer Timeout Handling

**Issue:** PRD Writer agent getting stuck with no error message

**Fix:** Added 10-minute timeout wrapper with proper error handling in `project_forge/src/orchestration/crew_config.py:lines/486-542`

Features:
- 10-minute (600 second) timeout for PRD writer tasks
- Clear error messages when timeout occurs
- Logging of all PRD writer operations
- Graceful error handling

If the PRD writer times out, you'll now see:
```
TimeoutError: README generation timed out after 10 minutes.
This may indicate an issue with the LLM API or the task complexity.
Try reducing max_iterations or simplifying your project idea.
```

### 3. Tracing & Observability Page

**New page:** "🔍 Tracing" in the navigation menu

Features:
- Configuration status checker
- Step-by-step setup instructions for LangSmith
- Alternative setup for LangFuse (open source)
- Guide on using traces to debug issues
- Troubleshooting section
- Quick links to tracing dashboards

Access it from the sidebar: **Navigation → 🔍 Tracing**

### 4. Tracing Utility Module

**New file:** `project_forge/src/utils/tracing_setup.py`

Utility functions:
- `setup_langsmith_tracing()` - Auto-configure LangSmith
- `setup_langfuse_tracing()` - Auto-configure LangFuse
- `setup_tracing()` - Set up all available backends
- `get_tracing_info()` - Get current configuration status

Usage:
```python
from project_forge.src.utils.tracing_setup import setup_tracing, get_tracing_info

# Auto-setup all configured backends
status = setup_tracing(verbose=True)

# Check configuration
info = get_tracing_info()
if info["langsmith"]["enabled"]:
    print(f"LangSmith project: {info['langsmith']['project']}")
```

## Debugging PRD Writer Issues

When the PRD writer gets stuck, use tracing to diagnose:

1. **Enable LangSmith** (see Quick Start above)

2. **Run your pipeline** that gets stuck

3. **Find the trace in LangSmith:**
   - Go to https://smith.langchain.com
   - Filter for recent runs
   - Look for "PRDWriter" or incomplete traces

4. **Analyze the trace:**
   - Check the last successful operation before hang
   - Look for error messages in sub-traces
   - Check token counts (large prompts may cause issues)
   - Review API latency (may indicate timeout)

5. **Common fixes:**
   - **Prompt too large:** Reduce max_iterations or simplify project
   - **API timeout:** Check OpenAI API status
   - **Memory issues:** Reduce project complexity
   - **Rate limits:** Wait and retry

## Environment Variables Reference

### Required
```bash
# OpenAI (required for all operations)
OPENAI_API_KEY=your_openai_api_key_here
```

### Tracing (Optional)
```bash
# LangSmith Tracing
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_PROJECT=project-forge
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com

# LangFuse Tracing (alternative)
LANGFUSE_PUBLIC_KEY=your_public_key
LANGFUSE_SECRET_KEY=your_secret_key
LANGFUSE_HOST=https://cloud.langfuse.com
```

## Additional Resources

### LangSmith
- Documentation: https://docs.smith.langchain.com
- Dashboard: https://smith.langchain.com
- Discord: https://discord.gg/langchain

### LangFuse (Open Source Alternative)
- Documentation: https://langfuse.com/docs
- Dashboard: https://cloud.langfuse.com
- GitHub: https://github.com/langfuse/langfuse
- Self-hosting: https://langfuse.com/docs/deployment/self-host

### CrewAI
- Documentation: https://docs.crewai.com
- Observability Guide: https://docs.crewai.com/core-concepts/Tools/

## Troubleshooting

### Traces not appearing?
1. Check environment variables are set correctly
2. Restart the Streamlit application
3. Verify API key is valid
4. Check network connectivity

### Still getting stuck at PRD Writer?
1. Check the Logs & Debug page for error details
2. Review traces in LangSmith for the exact failure point
3. Try reducing max_iterations (default is 2, try 1)
4. Simplify your project idea
5. Check OpenAI API status: https://status.openai.com

### Need help?
- Check the Tracing page in the UI for detailed guides
- Review captured logs in "Logs & Debug" page
- Open an issue on GitHub with trace links

## Testing the Fixes

To verify the fixes are working:

1. **Test DateTime Fix:**
   - Run any pipeline
   - Go to "Logs & Debug" page
   - Verify timing section displays correctly without errors

2. **Test PRD Writer Timeout:**
   - Run a Phase 4 pipeline
   - If it takes more than 10 minutes, you'll see a timeout error
   - Error message will be clear and actionable

3. **Test Tracing Setup:**
   - Go to "Tracing" page
   - Check configuration status
   - Follow setup instructions
   - Run a pipeline and view traces

## Summary of Changes

### Files Modified
- `streamlit_ui/pages/logs.py` - Fixed datetime TypeError
- `project_forge/src/orchestration/crew_config.py` - Added timeout handling
- `streamlit_app.py` - Added tracing page to navigation
- `.env.example` - Added tracing environment variables

### Files Created
- `streamlit_ui/pages/tracing.py` - New tracing configuration page
- `project_forge/src/utils/tracing_setup.py` - Tracing utility functions
- `TRACING_GUIDE.md` - This guide

All changes are backward compatible and optional. The system works without tracing enabled.
