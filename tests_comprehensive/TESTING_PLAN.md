# Project Forge - Comprehensive Testing Plan

## Overview
This document outlines all the testing opportunities for the Project Forge multi-agent system. It's written in plain English for intermediate programmers to understand what needs to be tested and why.

---

## 1. DATA MODELS TESTING

### What to Test: `project_forge/src/models/project_models.py`

**Why:** Data models are the foundation of the entire system. All agents read and write these models, so they must work correctly.

**Testing Opportunities:**

1. **ProjectIdea Model**
   - Can create an empty ProjectIdea with just raw_description
   - Can add refined_summary after creation
   - Can store constraints as a dictionary (like time, complexity, skill level)
   - Constraints dictionary handles different data types (strings, numbers, booleans)
   - Model can be serialized to JSON and back without data loss

2. **ProjectGoals Model**
   - Can create with empty lists for goals
   - Can add multiple learning goals as strings
   - Can add multiple technical goals as strings
   - Priority notes field accepts long text
   - Lists maintain order when items are added

3. **FrameworkChoice Model**
   - All fields can be None (for CLI-only projects)
   - Can set frontend, backend, storage independently
   - special_libs list can hold multiple library names
   - Model handles empty vs None correctly

4. **Step Model**
   - Index numbers are unique and sequential
   - Title is required and non-empty
   - Description can be long text
   - what_you_learn field can be empty initially
   - Dependencies list can contain multiple step indices
   - Dependencies don't create circular references

5. **Phase Model**
   - Index is between 1-5 (standard project structure)
   - Name and description are meaningful strings
   - Steps list can hold multiple Step objects
   - Can calculate total steps in a phase
   - Steps within a phase are ordered correctly

6. **ProjectPlan Model**
   - Combines all previous models correctly
   - Has exactly 5 phases (standard structure)
   - Total steps across all phases is around 50
   - All nested models maintain data integrity
   - teaching_notes field accepts markdown formatting

---

## 2. TOOLS TESTING

### What to Test: `project_forge/src/tools/`

**Why:** Tools provide utility functions that agents use. Bugs here affect multiple agents.

### 2.1 Text Cleaner Tool

**File:** `text_cleaner_tool.py`

1. **Basic Cleaning**
   - Removes extra whitespace correctly
   - Handles multiple newlines properly
   - Preserves intentional formatting
   - Handles empty strings without errors
   - Handles very long strings efficiently

2. **Edge Cases**
   - None input doesn't crash
   - String with only whitespace returns empty string
   - Unicode characters are preserved
   - Special characters don't break the cleaner
   - Very large text (10,000+ characters) processes correctly

### 2.2 Rubric Tool

**File:** `rubric_tool.py`

1. **Rubric Criteria**
   - All criteria enums are defined correctly
   - Each criterion has a scoring function
   - Score range is always 0-10
   - Pass threshold is reasonable for each criterion

2. **Concept Clarity Evaluation**
   - Scores detailed concepts higher than vague ones
   - Checks for specific technical terms
   - Identifies missing constraints
   - Provides actionable feedback
   - Handles edge cases (very short, very long concepts)

3. **Phase Balance Evaluation**
   - Detects when phases have too few steps (< 5)
   - Detects when phases have too many steps (> 15)
   - Ensures all phases have descriptions
   - Checks that step counts are reasonable
   - Provides specific feedback on imbalances

4. **Teaching Quality Evaluation**
   - Checks that steps have learning annotations
   - Measures quality of teaching notes
   - Ensures explanations are beginner-friendly
   - Identifies missing "why" explanations
   - Scores based on pedagogical value

### 2.3 Consistency Tool

**File:** `consistency_tool.py`

1. **Phase Count Validation**
   - Ensures exactly 5 phases exist
   - Phases are numbered 1-5 sequentially
   - No duplicate phase numbers
   - No missing phase numbers

2. **Step Count Validation**
   - Total steps across all phases is 40-60
   - Steps are numbered sequentially globally
   - No duplicate step numbers
   - Step dependencies reference valid step indices
   - No orphaned steps (all belong to a phase)

3. **Cross-Reference Validation**
   - Framework choice matches project goals
   - Phase complexity matches skill level
   - Teaching notes align with learning goals
   - Technical goals covered in implementation steps

---

## 3. AGENT TESTING

### What to Test: `project_forge/src/agents/`

**Why:** Agents are the core intelligence. Each agent transforms data in specific ways.

### 3.1 Concept Expander Agent

**File:** `concept_expander_agent.py`

1. **Agent Creation**
   - Agent can be instantiated successfully
   - Has correct role and goal defined
   - Backstory is appropriate for concept expansion
   - allow_delegation is set correctly

2. **Task Creation**
   - Task accepts raw project idea string
   - Task description includes the raw idea
   - Expected output format is clearly defined
   - Task is linked to correct agent

3. **Result Parsing**
   - Can parse valid JSON output from agent
   - Handles markdown code blocks around JSON
   - Creates valid ProjectIdea object
   - Falls back gracefully on parsing errors
   - Extracts refined_summary correctly
   - Captures constraints dictionary

4. **Integration Tests**
   - Simple idea: "Build a todo app" → produces clear refined summary
   - Complex idea: Long paragraph → extracts key points
   - Vague idea: "Something with AI" → asks clarifying details
   - Constraints extraction: Mentions "beginner" → adds to constraints
   - Constraints extraction: Mentions "1 week" → adds time constraint

### 3.2 Goals Analyzer Agent

**File:** `goals_analyzer_agent.py`

1. **Agent Creation**
   - Agent instantiates with correct configuration
   - Role focuses on extracting learning objectives
   - Goal emphasizes both learning and technical goals

2. **Task Creation**
   - Task receives ProjectIdea as input
   - Task description requests separate goal types
   - Output format specifies lists of goals

3. **Result Parsing**
   - Parses JSON with learning_goals array
   - Parses JSON with technical_goals array
   - Creates valid ProjectGoals object
   - Handles empty goal lists
   - Handles parsing errors gracefully

4. **Integration Tests**
   - Educational project → extracts learning goals
   - Technical project → extracts technical deliverables
   - Mixed project → separates both types correctly
   - Priority notes capture important constraints
   - Goals align with refined project concept

### 3.3 Framework Selector Agent

**File:** `framework_selector_agent.py`

1. **Agent Creation**
   - Agent configured for framework selection
   - Understands skill levels (beginner/intermediate/advanced)
   - Prefers simple, well-documented tools

2. **Task Creation**
   - Task receives ProjectIdea and ProjectGoals
   - Task includes skill level context
   - Task requests specific framework choices

3. **Result Parsing**
   - Parses framework choices correctly
   - Creates valid FrameworkChoice object
   - Handles optional fields (frontend can be None)
   - Parses special_libs array

4. **Integration Tests**
   - Beginner + web app → suggests Streamlit (not Flask)
   - Intermediate + API → suggests FastAPI
   - Advanced + complex → suggests appropriate tools
   - CLI-only project → frontend is None
   - Data storage needs → suggests SQLite for simple, Postgres for complex

### 3.4 Phase Designer Agent

**File:** `phase_designer_agent.py`

1. **Agent Creation**
   - Agent configured for creating structured plans
   - Understands 5-phase, 50-step structure
   - Keeps steps small and concrete

2. **Task Creation**
   - Task receives all previous outputs (idea, goals, framework)
   - Task specifies exactly 5 phases
   - Task requests ~10 steps per phase

3. **Result Parsing**
   - Parses nested JSON structure (phases with steps)
   - Creates valid ProjectPlan object
   - All phases have correct indices
   - All steps have correct indices
   - Dependencies are valid step indices

4. **Integration Tests**
   - Creates exactly 5 phases
   - Total steps is 40-60
   - Phases are logically ordered (setup → core → polish)
   - Steps within phases are coherent
   - Dependencies make sense (setup before features)
   - Step descriptions are actionable

### 3.5 Teacher Agent

**File:** `teacher_agent.py`

1. **Agent Creation**
   - Agent configured with teaching expertise
   - Focuses on pedagogical value
   - Explains "what you'll learn" for each step

2. **Task Creation**
   - Task receives ProjectPlan with phases
   - Task requests teaching annotations
   - Task emphasizes learning outcomes

3. **Result Parsing**
   - Updates existing ProjectPlan with annotations
   - Adds what_you_learn to each step
   - Adds global teaching_notes
   - Preserves existing plan structure

4. **Integration Tests**
   - Adds meaningful learning notes to steps
   - Notes explain concepts, not just actions
   - Beginner-friendly explanations for simple projects
   - Advanced concepts for complex projects
   - Global teaching notes tie everything together

### 3.6 Evaluator Agent

**File:** `evaluator_agent.py`

1. **Evaluation Functions**
   - evaluate_project_plan() returns EvaluationResult
   - Uses rubric tool for scoring
   - Checks multiple quality criteria
   - Provides actionable feedback

2. **Quality Checks**
   - Concept clarity is evaluated
   - Phase balance is checked
   - Teaching quality is assessed
   - Technical feasibility is verified
   - Completeness is confirmed

3. **Approval Logic**
   - Approves when all criteria pass thresholds
   - Provides specific feedback on failures
   - Suggests concrete improvements
   - Handles edge cases (perfect vs terrible plans)

4. **Integration Tests**
   - Good plan → approved with high scores
   - Unbalanced phases → rejected with feedback
   - Missing teaching notes → rejected with specific guidance
   - Too ambitious → rejected as infeasible
   - Multiple issues → all are identified in feedback

### 3.7 PRD Writer Agent

**File:** `prd_writer_agent.py`

1. **Agent Creation**
   - Agent configured for technical writing
   - Understands README/PRD format
   - Includes all necessary sections

2. **Task Creation**
   - Task receives approved ProjectPlan
   - Task specifies README format
   - Task requests markdown output

3. **Result Parsing**
   - Extracts README text from agent output
   - Generates appropriate project name
   - Cleans markdown formatting
   - Preserves code blocks and lists

4. **Integration Tests**
   - README includes all required sections
   - Teaching notes are embedded per step
   - Framework choices are documented
   - Phases and steps are clearly formatted
   - README is valid markdown
   - README is comprehensive (5000+ characters)

---

## 4. ORCHESTRATION TESTING

### What to Test: `project_forge/src/orchestration/`

**Why:** Orchestration connects all agents. This is where the pipeline can break.

### 4.1 Crew Configuration

**File:** `crew_config.py`

1. **Planning Crew (Phase 2)**
   - Creates all three planning agents
   - Executes tasks in correct order
   - Passes data between agents correctly
   - Returns valid PlanningResult
   - Handles agent failures gracefully

2. **Full Plan Crew (Phase 3)**
   - Creates all six planning agents
   - Includes evaluation in pipeline
   - Supports multiple iterations for refinement
   - Returns valid FullPlanResult
   - Iteration limit prevents infinite loops

3. **Complete Pipeline (Phase 4)**
   - Creates all seven agents including PRD writer
   - Executes full pipeline end-to-end
   - Generates README output
   - Returns valid FullPlanWithReadmeResult
   - Handles errors at any stage

4. **Integration Tests**
   - Simple idea → complete README in one iteration
   - Complex idea → multiple refinement iterations
   - Invalid input → clear error messages
   - API failures → retry logic works
   - Partial completion → state is preserved

### 4.2 CLI Runner

**File:** `runner.py`

1. **Argument Parsing**
   - Parses project idea from command line
   - Handles skill level flag correctly
   - Handles complexity flag correctly
   - Handles project type flag correctly
   - Handles all optional flags
   - Handles stdin input (piped data)

2. **Input Validation**
   - Rejects empty project ideas
   - Rejects very short ideas (< 10 chars)
   - Checks for OPENAI_API_KEY environment variable
   - Validates output directory permissions
   - Provides clear error messages

3. **Logging Setup**
   - Creates logger with correct level
   - Verbose flag increases logging detail
   - Logs are formatted properly
   - Logs include timestamps and agent names

4. **Pipeline Execution**
   - Phase 2 runs planning crew only
   - Phase 3 runs full plan crew
   - Phase 4 runs complete pipeline
   - Each phase displays appropriate summary
   - Execution time is tracked

5. **Error Handling**
   - Keyboard interrupt exits gracefully
   - API errors show helpful messages
   - File errors are caught and explained
   - Permission errors guide user to fix
   - Unexpected errors show stack trace

6. **Output Generation**
   - Creates output directory if missing
   - Generates unique filename with project name
   - Writes README with correct encoding (UTF-8)
   - Displays output path to user
   - File size is reported

7. **Integration Tests**
   - Complete flow: idea → README file
   - Skill level affects output (beginner vs advanced)
   - Complexity affects scope
   - Project type affects detail level
   - Verbose flag shows more logging
   - Invalid API key shows clear error
   - Missing output directory is created

---

## 5. STREAMLIT UI TESTING

### What to Test: `streamlit_app.py` and `streamlit_ui/`

**Why:** UI is the user's first impression. It must work smoothly.

### 5.1 Main App

**File:** `streamlit_app.py`

1. **Page Configuration**
   - Page loads without errors
   - Title and icon display correctly
   - Layout is wide mode
   - Sidebar is expanded by default

2. **Navigation**
   - All navigation options are present
   - Clicking each option loads correct page
   - Page state persists during navigation
   - No errors when switching pages rapidly

3. **Session State**
   - Session state initializes correctly
   - Execution status is tracked
   - Agent completion status is tracked
   - Progress percentage updates
   - State persists across page changes

4. **Sidebar Status Display**
   - Shows current agent when running
   - Shows progress bar correctly
   - Shows completion status for each agent
   - Updates in real-time during execution

### 5.2 Home Page

**File:** `streamlit_ui/pages/home.py`

1. **UI Elements**
   - Welcome message displays
   - Input box for project idea
   - Skill level selector works
   - Complexity selector works
   - Run button is clickable

2. **Execution Trigger**
   - Button click starts pipeline
   - Input validation prevents empty ideas
   - Loading state shows during execution
   - Error messages display if execution fails

3. **Results Display**
   - Summary shows after completion
   - All agent outputs are accessible
   - README preview is formatted correctly
   - Download button works

### 5.3 Agent Pages

**Files:** `streamlit_ui/pages/concept_expander.py`, etc.

1. **Concept Expander Page**
   - Displays raw idea input
   - Shows refined summary output
   - Displays extracted constraints
   - Shows before/after comparison

2. **Goals Analyzer Page**
   - Lists learning goals clearly
   - Lists technical goals separately
   - Shows priority notes
   - Format is readable

3. **Framework Selector Page**
   - Displays chosen frontend
   - Displays chosen backend
   - Displays storage choice
   - Lists special libraries
   - Explains why each was chosen

4. **Phase Designer Page**
   - Shows all 5 phases
   - Each phase shows its steps
   - Steps have indices and titles
   - Dependencies are visualized
   - Can expand/collapse phases

5. **Teacher Agent Page**
   - Shows teaching annotations per step
   - Displays global teaching notes
   - Highlights learning outcomes
   - Format is pedagogically clear

6. **Evaluator Agent Page**
   - Shows evaluation scores
   - Displays feedback for each criterion
   - Shows pass/fail status
   - Explains what needs improvement

7. **PRD Writer Page**
   - Displays full README content
   - Markdown is rendered correctly
   - Code blocks are formatted
   - Download button works
   - Copy to clipboard works

### 5.4 Logs Page

**File:** `streamlit_ui/pages/logs.py`

1. **Log Display**
   - Shows execution logs chronologically
   - Filters by log level work
   - Search functionality works
   - Logs update in real-time
   - Can clear logs

---

## 6. END-TO-END INTEGRATION TESTING

**Why:** Individual components may work, but the full system must work together seamlessly.

### 6.1 Happy Path Tests

1. **Simple Todo App**
   - Input: "Build a todo app"
   - Skill: Beginner
   - Expected: Streamlit-based, simple storage, clear steps
   - Verify: README is generated successfully

2. **Intermediate Web Scraper**
   - Input: "Create a web scraper for job postings with async requests"
   - Skill: Intermediate
   - Expected: BeautifulSoup, async libraries, proper error handling
   - Verify: Teaching notes explain async concepts

3. **Advanced Multi-Agent System**
   - Input: "Build a CrewAI system for code review"
   - Skill: Advanced
   - Expected: CrewAI, LangChain, complex architecture
   - Verify: 5 phases, ~50 steps, comprehensive plan

### 6.2 Edge Case Tests

1. **Minimal Input**
   - Input: "Todo app"
   - Verify: System expands minimal idea into full concept

2. **Maximum Input**
   - Input: Very detailed 500-word description
   - Verify: System extracts key points, doesn't get overwhelmed

3. **Vague Input**
   - Input: "Something with AI"
   - Verify: System asks for clarification or makes reasonable assumptions

4. **Conflicting Requirements**
   - Input: "Beginner-level complex distributed system"
   - Verify: System reconciles conflict reasonably

### 6.3 Error Recovery Tests

1. **API Timeout**
   - Simulate: Network timeout during agent execution
   - Verify: System retries or fails gracefully with message

2. **Invalid API Key**
   - Setup: Wrong or missing OPENAI_API_KEY
   - Verify: Clear error message before pipeline starts

3. **Parsing Failure**
   - Simulate: Agent returns malformed JSON
   - Verify: Fallback behavior activates, user informed

4. **Disk Full**
   - Simulate: No space to write README
   - Verify: Clear error about disk space

### 6.4 Performance Tests

1. **Execution Time**
   - Measure: Total time from input to README
   - Expected: < 5 minutes for standard project
   - Verify: Times out appropriately if too long

2. **Memory Usage**
   - Measure: Memory consumption during execution
   - Expected: < 500MB for standard run
   - Verify: No memory leaks over multiple runs

3. **Concurrent Execution**
   - Test: Multiple Streamlit users running simultaneously
   - Verify: Sessions don't interfere with each other

---

## 7. CONFIGURATION AND DATA TESTING

### 7.1 Configuration Files

**File:** `project_forge/src/config/defaults.yaml` (if exists)

1. **File Loading**
   - YAML file loads without errors
   - All expected keys are present
   - Values are correct types

2. **Skill Presets**
   - Beginner preset has appropriate settings
   - Intermediate preset is more complex
   - Advanced preset enables all features

3. **Framework Templates**
   - Templates for common stacks exist
   - Templates are valid and complete

### 7.2 Example Data

**Files:** Example READMEs and inputs

1. **Example Inputs**
   - All example inputs generate valid output
   - Examples cover different project types
   - Examples demonstrate all features

2. **Example Outputs**
   - Example READMEs are well-formatted
   - They match current output format
   - They demonstrate best practices

---

## 8. DEPENDENCY AND ENVIRONMENT TESTING

### 8.1 Requirements

**File:** `requirements.txt`

1. **Installation**
   - All packages install without errors
   - Version constraints are satisfied
   - No conflicting dependencies

2. **Import Tests**
   - All Python modules can be imported
   - No missing dependencies at runtime

### 8.2 Environment Variables

1. **API Keys**
   - OPENAI_API_KEY is checked before execution
   - Clear error if missing
   - Supports .env file loading

2. **Optional Variables**
   - LOG_LEVEL can override default
   - OUTPUT_DIR can be customized

---

## 9. SECURITY AND SAFETY TESTING

**Why:** Prevent common vulnerabilities and ensure safe execution.

1. **Input Sanitization**
   - Reject potentially malicious input strings
   - Handle SQL injection attempts (even though we don't use SQL)
   - Handle path traversal in output filename
   - Validate all user inputs

2. **Output Safety**
   - Generated code doesn't contain obvious vulnerabilities
   - No hardcoded credentials in output
   - Safe file handling (no arbitrary file writes)

3. **API Key Protection**
   - API keys not logged in verbose mode
   - Keys not included in output files
   - Keys not exposed in error messages

---

## 10. DOCUMENTATION AND USABILITY TESTING

**Why:** Good docs and UX prevent user confusion.

1. **README Quality**
   - README explains what Project Forge does
   - Setup instructions are clear and complete
   - Examples are provided and work
   - Common issues are documented

2. **Error Messages**
   - All error messages are clear
   - Errors suggest how to fix the problem
   - No cryptic technical jargon for user errors

3. **Help Text**
   - Command-line help is comprehensive
   - All flags are documented
   - Examples are provided

---

## Testing Priority Levels

### CRITICAL (Must Pass)
- Data models serialize/deserialize correctly
- All agents can be created and execute tasks
- CLI runner executes without crashing
- Complete pipeline generates a README
- Output file is created successfully

### HIGH (Should Pass)
- Agent parsing handles malformed JSON
- Input validation catches bad inputs
- Error messages are clear and helpful
- Integration tests pass for common scenarios
- Streamlit UI loads without errors

### MEDIUM (Nice to Have)
- Performance within acceptable limits
- All rubric criteria work correctly
- Logs are detailed and helpful
- Example inputs all work
- UI is responsive and intuitive

### LOW (Can Defer)
- Advanced error recovery
- Concurrent execution handling
- Extreme edge cases
- Optimization for speed

---

## Next Steps

After understanding this testing plan:
1. Review each section to understand what needs testing
2. Build a test suite that covers critical and high-priority items
3. Run the tests and document results
4. Fix any failures
5. Re-run until all critical tests pass

This plan provides a roadmap for thorough testing without requiring deep technical knowledge of testing frameworks. Each test can be implemented as a simple Python function that checks expected behavior.
