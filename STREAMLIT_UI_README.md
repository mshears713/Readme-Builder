# Project Forge - Streamlit UI

Interactive web interface for the Project Forge Multi-Agent README Generator.

## Overview

This Streamlit application provides a comprehensive UI for interacting with the Project Forge multi-agent system. It allows users to:

- Input project ideas through an intuitive form
- Track real-time agent execution progress
- View detailed outputs from each of the 7 agents
- Explore agent reasoning and processing steps
- Access debugging logs and error information
- Download generated README files

## Features

### 🏠 Home Page
- User input form for project ideas
- Configuration options (skill level, phase, iterations)
- Real-time execution progress tracking
- Results display with tabbed interface
- README download capability

### 📝 Agent Detail Pages

Each of the 7 agents has a dedicated page showing:

1. **Concept Expander** - Project idea refinement and constraints
2. **Goals Analyzer** - Learning and technical objectives
3. **Framework Selector** - Technology stack recommendations
4. **Phase Designer** - 5-phase build plan structure
5. **Teacher Agent** - Pedagogical annotations
6. **Evaluator Agent** - Quality scores and approval status
7. **PRD Writer** - Final README generation

Each page displays:
- **Input**: What data the agent received
- **Processing**: How the agent transformed the data
- **Output**: The agent's final result
- **Logs**: Agent-specific execution logs

### 🔍 Logs & Debug Page
- Execution logs with filtering
- Agent-specific log viewing
- Captured stdout/stderr
- Error messages and troubleshooting
- Debug information export

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   Create a `.env` file with your API keys:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

## Usage

### Running the UI

**Option 1: Direct command**
```bash
streamlit run streamlit_app.py
```

**Option 2: Using the run script**
```bash
chmod +x run_streamlit.sh
./run_streamlit.sh
```

The UI will open in your default browser at `http://localhost:8501`

### Using the Application

1. **Navigate to Home Page**
   - Enter your project idea in the text area
   - Select skill level (beginner/intermediate/advanced)
   - Choose pipeline phase (2, 3, or 4)
   - Set max iterations for refinement
   - Click "Run Pipeline"

2. **Monitor Progress**
   - Watch the sidebar for agent progress
   - View real-time execution status
   - Check elapsed time and current agent

3. **Explore Results**
   - Use tabs on Home page for quick overview
   - Navigate to individual agent pages for detailed views
   - Check Logs & Debug for troubleshooting

4. **Download README**
   - Once execution completes, download the README
   - README available from Home page or PRD Writer page

## Project Structure

```
Readme-Builder/
├── streamlit_app.py              # Main Streamlit application
├── streamlit_ui/                 # UI package
│   ├── __init__.py
│   ├── utils.py                  # Utility functions and helpers
│   └── pages/                    # Individual page modules
│       ├── __init__.py
│       ├── home.py               # Home page with input form
│       ├── concept_expander.py   # Concept Expander agent page
│       ├── goals_analyzer.py     # Goals Analyzer agent page
│       ├── framework_selector.py # Framework Selector agent page
│       ├── phase_designer.py     # Phase Designer agent page
│       ├── teacher_agent.py      # Teacher Agent page
│       ├── evaluator_agent.py    # Evaluator Agent page
│       ├── prd_writer.py         # PRD Writer agent page
│       └── logs.py               # Logs and debugging page
├── project_forge/                # Agent system (existing)
│   └── src/
│       ├── agents/               # 7 agent implementations
│       ├── models/               # Data models
│       ├── orchestration/        # Pipeline orchestration
│       └── tools/                # Utility tools
└── requirements.txt              # Python dependencies
```

## Architecture

### Session State Management

The UI uses Streamlit's session state to track:
- Execution progress and status
- Agent outputs and results
- Logs and debugging information
- User input parameters

### Data Flow

```
User Input → Home Page → Pipeline Execution → Session State → Agent Pages
                                ↓
                         Logs & Debug Page
```

### Agent Execution

The UI runs the Project Forge pipeline in the main thread and captures:
- Agent outputs (via orchestration results)
- Execution logs (via logging module)
- stdout/stderr (via output capture)
- Errors and exceptions (via try/catch)

## Configuration

### Streamlit Config

Create `.streamlit/config.toml` for custom settings:

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[server]
port = 8501
headless = false
```

### Environment Variables

Required:
- `ANTHROPIC_API_KEY` - Your Anthropic API key for Claude

Optional:
- `LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)

## Troubleshooting

### Common Issues

1. **Import errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python path includes project root

2. **API errors**
   - Verify `ANTHROPIC_API_KEY` is set correctly
   - Check API key has sufficient credits

3. **UI not updating**
   - Use the "Rerun" button in Streamlit
   - Check browser console for errors

4. **Execution hangs**
   - Check Logs & Debug page for errors
   - Reduce `max_iterations` setting
   - Verify LLM API is responding

### Debug Mode

Enable verbose logging:
1. Check "Verbose Output" in Home page form
2. View detailed logs in Logs & Debug page
3. Export debug snapshot for troubleshooting

## Development

### Adding New Features

1. **New agent page:**
   - Create file in `streamlit_ui/pages/`
   - Follow existing agent page template
   - Add import in `streamlit_app.py`
   - Add navigation menu item

2. **New utility function:**
   - Add to `streamlit_ui/utils.py`
   - Import in relevant pages
   - Update type hints and docstrings

3. **Custom styling:**
   - Add CSS in `streamlit_app.py` markdown
   - Use Streamlit components for widgets
   - Follow existing color scheme

### Testing

Test the UI manually by:
1. Running with sample project ideas
2. Testing all navigation pages
3. Verifying error handling
4. Checking log display
5. Testing download functionality

## Performance

### Optimization Tips

1. **Cache framework config:**
   - Use `@st.cache_resource` for config loading
   - Reuse loaded configurations

2. **Lazy loading:**
   - Only render active page/tab
   - Defer heavy computations

3. **Session state:**
   - Store results to avoid re-execution
   - Clear old data when starting new run

4. **Update frequency:**
   - Limit UI updates to ~1Hz during execution
   - Batch state updates

## Contributing

To contribute to the Streamlit UI:

1. Follow existing code style and patterns
2. Add docstrings to all functions
3. Test thoroughly with different inputs
4. Update this README with new features

## License

Part of the Project Forge project. See main project LICENSE for details.

## Support

For issues or questions:
1. Check the Logs & Debug page for error details
2. Review this README for common issues
3. Check Project Forge documentation
4. Open an issue in the repository

---

**Version:** 1.0
**Last Updated:** November 17, 2025
**Powered by:** Streamlit, CrewAI, Claude
