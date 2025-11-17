# Habit Tracker App with Streamlit

## Overview

A simple, beginner-friendly habit tracking application built with Streamlit that helps users build and maintain positive habits through daily check-ins, visual streak tracking, and motivational feedback. This project is designed to teach core web development concepts, data persistence, and user interface design while building something immediately useful.

The app will allow users to:
- Create and manage multiple habits with custom names and goals
- Mark habits as complete each day with simple checkbox interactions
- View visual streak charts showing consistency over time
- Get encouraging feedback and insights about their progress
- Persist data locally so habits are saved between sessions

This is an excellent first web application project that introduces Streamlit's reactive programming model, basic data structures, file-based storage, and creating engaging user experiences.

## Teaching Goals

### Learning Goals
- **Streamlit Fundamentals**: Understand Streamlit's reactive model, widgets, and layout system
- **Data Persistence**: Learn how to save and load data using JSON files
- **Date/Time Handling**: Work with Python's datetime module for tracking daily habits
- **Data Visualization**: Create simple charts to show habit streaks and progress
- **State Management**: Manage application state across user interactions

### Technical Goals
- Build a complete web application with user input and data display
- Implement CRUD operations (Create, Read, Update, Delete) for habits
- Design an intuitive user interface with clear visual feedback
- Handle edge cases like missing data and date transitions
- Structure code in a maintainable, modular way

### Priority Notes
Focus on simplicity and user experience over advanced features. The goal is to build confidence with web development basics and create something genuinely useful. Visual feedback (streaks, charts) makes progress tangible and keeps learners engaged.

## Technology Stack

**Frontend**: Streamlit
- Reason: Streamlit is perfect for beginners because you write Python, not HTML/CSS/JavaScript
- Provides instant visual feedback as you code
- Built-in widgets make forms and inputs trivial
- Great documentation and community examples

**Backend**: Streamlit (built-in)
- Streamlit handles server logic automatically
- No need for separate backend framework
- Focus on application logic, not infrastructure

**Storage**: JSON files
- Simple text files that are easy to inspect and debug
- No database setup required
- Python's json module makes reading/writing trivial
- Perfect for single-user applications

**Key Libraries**:
- `streamlit`: Web UI framework
- `json`: Data persistence
- `datetime`: Date tracking and calculations
- `pandas`: Data manipulation and chart preparation
- `pathlib`: File path handling

## Architecture Overview

```
┌─────────────────────────────────────────┐
│          Streamlit Web UI               │
│  (Input Forms, Checkboxes, Charts)      │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│       Application Logic Layer           │
│  - Habit management functions           │
│  - Streak calculation                   │
│  - Data validation                      │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│        Data Persistence Layer           │
│    (habits.json in local directory)     │
└─────────────────────────────────────────┘
```

The application follows a simple three-layer architecture:
1. **UI Layer**: Streamlit widgets for user interaction
2. **Logic Layer**: Pure Python functions that manipulate habit data
3. **Storage Layer**: JSON file read/write operations

This separation makes the code easy to understand, test, and modify.

## Implementation Plan

### Phase 1: Project Setup & Core Data Models (10 steps)

**1. Create project directory structure**
   - Set up folders for the app, data, and tests
   - Create requirements.txt with initial dependencies
   - Initialize git repository for version control
   - **What You'll Learn**: Project organization best practices, dependency management
   - Dependencies: None

**2. Define the Habit data structure**
   - Create a Python dataclass or dictionary schema for a Habit
   - Include fields: name, created_date, goal_frequency, completion_dates
   - Write docstrings explaining each field
   - **What You'll Learn**: Data modeling, choosing appropriate data structures
   - Dependencies: None

**3. Implement JSON file reading function**
   - Write load_habits() function to read from habits.json
   - Handle the case where the file doesn't exist yet (return empty list)
   - Add error handling for malformed JSON
   - **What You'll Learn**: File I/O, exception handling, defensive programming
   - Dependencies: 2

**4. Implement JSON file writing function**
   - Write save_habits() function to persist habits to habits.json
   - Use json.dump() with pretty printing (indent=2) for readability
   - Ensure atomic writes to prevent data corruption
   - **What You'll Learn**: File writing, data serialization, atomicity concepts
   - Dependencies: 2

**5. Create helper function to initialize new habit**
   - Function: create_new_habit(name, goal_frequency) → Habit
   - Generate unique ID, set creation date to today
   - Initialize empty completion_dates list
   - **What You'll Learn**: Factory functions, date handling with datetime.date.today()
   - Dependencies: 2

**6. Create basic Streamlit app file (app.py)**
   - Import streamlit and set page config (title, icon, layout)
   - Add a title and welcome message
   - Run with `streamlit run app.py` to verify setup
   - **What You'll Learn**: Streamlit basics, running web apps locally
   - Dependencies: None

**7. Add session state initialization**
   - Use st.session_state to store loaded habits
   - Load habits from JSON on first run
   - Understand Streamlit's re-running behavior
   - **What You'll Learn**: Streamlit session state, managing application state
   - Dependencies: 3, 6

**8. Create sidebar for navigation**
   - Add st.sidebar with radio buttons: "My Habits", "Add New Habit", "Statistics"
   - Store selected page in session state
   - **What You'll Learn**: Streamlit layouts, navigation patterns
   - Dependencies: 6

**9. Write unit tests for data functions**
   - Test load_habits() with missing file and valid file
   - Test save_habits() creates file correctly
   - Test create_new_habit() generates correct structure
   - **What You'll Learn**: Unit testing with pytest, test-driven development
   - Dependencies: 3, 4, 5

**10. Add logging and error display**
   - Configure Python logging module
   - Display user-friendly error messages with st.error() when operations fail
   - Log errors to console for debugging
   - **What You'll Learn**: Logging best practices, user experience during errors
   - Dependencies: 6

### Phase 2: Core Habit Management Features (10 steps)

**11. Build "Add New Habit" form**
   - Text input for habit name
   - Select box for frequency goal (Daily, Weekly, etc.)
   - Submit button that calls create_new_habit()
   - **What You'll Learn**: Streamlit forms, user input validation
   - Dependencies: 5, 8

**12. Add habit to session state and save to file**
   - On form submit, append new habit to session state
   - Call save_habits() to persist
   - Display success message with st.success()
   - **What You'll Learn**: State mutations, data persistence flow
   - Dependencies: 4, 7, 11

**13. Display habit list on "My Habits" page**
   - Loop through habits in session state
   - Display each habit name and creation date
   - Show "No habits yet" message if list is empty
   - **What You'll Learn**: Streamlit layouts, conditional rendering
   - Dependencies: 7, 8

**14. Add daily check-in checkbox for each habit**
   - For each habit, show a checkbox: "Did you do [habit] today?"
   - Check if today's date is already in completion_dates
   - Pre-check the box if completed today
   - **What You'll Learn**: Dynamic UI generation, date comparisons
   - Dependencies: 13

**15. Handle checkbox state changes (mark complete/incomplete)**
   - On checkbox toggle, add or remove today's date from completion_dates
   - Save updated habits to JSON
   - Use st.rerun() if needed to refresh UI
   - **What You'll Learn**: Event handling in Streamlit, data updates
   - Dependencies: 4, 14

**16. Calculate current streak for a habit**
   - Function: calculate_streak(completion_dates) → int
   - Count consecutive days backwards from today
   - Handle missing dates and date gaps correctly
   - **What You'll Learn**: Date arithmetic, algorithm design
   - Dependencies: None

**17. Display current streak next to each habit**
   - Call calculate_streak() for each habit
   - Show streak count with emoji: "🔥 5 day streak!"
   - Highlight long streaks with different colors
   - **What You'll Learn**: Data presentation, visual feedback
   - Dependencies: 13, 16

**18. Add delete habit functionality**
   - Show a delete button (or expander with confirmation) for each habit
   - Remove habit from session state and save
   - Show confirmation dialog to prevent accidental deletes
   - **What You'll Learn**: CRUD operations, confirmation patterns
   - Dependencies: 4, 7, 13

**19. Implement habit editing (rename)**
   - Allow users to click an "Edit" button to rename a habit
   - Use st.text_input with current name as default
   - Update habit name in session state and save
   - **What You'll Learn**: In-place editing, form state management
   - Dependencies: 4, 7, 13

**20. Add input validation and error handling**
   - Prevent duplicate habit names
   - Require non-empty habit names
   - Show helpful error messages with st.warning()
   - **What You'll Learn**: Input validation, user-friendly error messages
   - Dependencies: 11, 19

### Phase 3: Visualization & Statistics (10 steps)

**21. Create "Statistics" page structure**
   - Add header and description for statistics section
   - Show overall completion rate across all habits
   - Display total number of habits tracked
   - **What You'll Learn**: Dashboard layouts, aggregate statistics
   - Dependencies: 8

**22. Calculate total completions per habit**
   - Function: get_total_completions(habit) → int
   - Simply return len(completion_dates)
   - Display as a metric for each habit
   - **What You'll Learn**: Basic aggregation, metrics display
   - Dependencies: None

**23. Calculate completion rate for last 7 days**
   - Function: get_weekly_rate(habit) → float (0.0 to 1.0)
   - Check how many of last 7 days have completion records
   - Handle cases where habit is newer than 7 days
   - **What You'll Learn**: Rolling window calculations, percentage formatting
   - Dependencies: None

**24. Display weekly completion rates with st.metric()**
   - For each habit, show last 7 days completion as percentage
   - Use st.metric() with delta to show trend
   - Color-code: green for improving, red for declining
   - **What You'll Learn**: Streamlit metrics, trend visualization
   - Dependencies: 21, 23

**25. Prepare data for line chart (completions over time)**
   - Convert completion_dates to a pandas DataFrame
   - Create date range for last 30 days
   - Count completions per day
   - **What You'll Learn**: pandas basics, data preparation for visualization
   - Dependencies: None

**26. Create line chart showing habit completion over time**
   - Use st.line_chart() with prepared DataFrame
   - Show last 30 days of data
   - Add axis labels and title
   - **What You'll Learn**: Data visualization, time series charts
   - Dependencies: 25

**27. Add calendar heatmap visualization**
   - Use Plotly or Altair to create a GitHub-style contribution heatmap
   - Color squares by completion status (green = done, gray = missed)
   - Show last 90 days in calendar grid
   - **What You'll Learn**: Advanced visualizations, third-party charting libraries
   - Dependencies: None

**28. Display heatmap with st.plotly_chart() or st.altair_chart()**
   - Integrate the heatmap into the Statistics page
   - Make it interactive (hover shows date and status)
   - **What You'll Learn**: Interactive charts, Streamlit chart components
   - Dependencies: 27

**29. Add "best streak" and "longest streak" statistics**
   - Function: calculate_longest_streak(completion_dates) → int
   - Iterate through all date ranges to find longest consecutive run
   - Display as highlighted metrics on Statistics page
   - **What You'll Learn**: Algorithm optimization, historical data analysis
   - Dependencies: 16, 21

**30. Create motivational insights**
   - Generate messages based on streaks: "You're on fire! 🔥"
   - Show encouragement for getting back on track
   - Display randomly chosen motivational quotes
   - **What You'll Learn**: Dynamic content generation, gamification principles
   - Dependencies: 21, 29

### Phase 4: Polish & User Experience (10 steps)

**31. Add date range filter for statistics**
   - Sidebar date picker: select start and end dates
   - Filter all statistics to only show selected date range
   - Default to "Last 30 days"
   - **What You'll Learn**: Date filtering, UI controls for data exploration
   - Dependencies: 21

**32. Implement habit sorting and filtering**
   - Allow sorting by name, streak, creation date
   - Filter to show only active habits or all habits
   - Use st.selectbox for sort options
   - **What You'll Learn**: Data sorting, filtering patterns
   - Dependencies: 13

**33. Add visual theme and color customization**
   - Use st.set_page_config() to set color theme
   - Add custom CSS with st.markdown() for styling
   - Choose colors that are motivating and easy on the eyes
   - **What You'll Learn**: Streamlit theming, basic CSS
   - Dependencies: 6

**34. Create data export functionality**
   - Add "Download Data" button on Statistics page
   - Export habits data as CSV using pandas
   - Use st.download_button() to trigger download
   - **What You'll Learn**: Data export, CSV generation, pandas I/O
   - Dependencies: 21

**35. Add data import functionality**
   - Upload CSV button to import habits from another device
   - Parse CSV and merge with existing habits
   - Handle duplicate habits intelligently
   - **What You'll Learn**: File uploads in Streamlit, data merging
   - Dependencies: 7

**36. Implement habit categories/tags**
   - Add optional category field to habit data model (Health, Work, etc.)
   - Show category badges next to habit names
   - Filter habits by category
   - **What You'll Learn**: Data model evolution, categorical data
   - Dependencies: 2, 13

**37. Add habit notes/journal feature**
   - Allow users to add optional notes when checking in
   - Store notes with completion date
   - Display notes in an expander on Statistics page
   - **What You'll Learn**: Rich data capture, text storage
   - Dependencies: 2, 15

**38. Create weekly summary email/notification (optional)**
   - Generate text summary of week's completions
   - Show in app, or optionally send via email (using smtplib)
   - Include motivation and next week's goals
   - **What You'll Learn**: Email automation (optional), report generation
   - Dependencies: 23, 29

**39. Add keyboard shortcuts for quick check-ins**
   - Use Streamlit experimental keyboard features or buttons
   - Allow pressing "1", "2", "3" to quickly check habits 1, 2, 3
   - Display keyboard hint in UI
   - **What You'll Learn**: Accessibility, power user features
   - Dependencies: 14

**40. Comprehensive testing and bug fixes**
   - Test with multiple habits and long date ranges
   - Fix edge cases (leap years, timezone issues, etc.)
   - Ensure UI is responsive and loads quickly
   - Write integration tests for full workflows
   - **What You'll Learn**: QA process, edge case handling, integration testing
   - Dependencies: All previous steps

### Phase 5: Deployment & Documentation (10 steps)

**41. Write comprehensive README.md**
   - Installation instructions
   - Usage guide with screenshots
   - Feature list and roadmap
   - **What You'll Learn**: Technical documentation, README best practices
   - Dependencies: None

**42. Add requirements.txt with pinned versions**
   - Lock all dependency versions for reproducibility
   - Include Python version requirement
   - Add optional dependencies section
   - **What You'll Learn**: Dependency management, reproducible environments
   - Dependencies: None

**43. Create example habits.json for new users**
   - Include 2-3 sample habits so app isn't empty on first run
   - Add comments (in separate file) explaining structure
   - **What You'll Learn**: User onboarding, example data
   - Dependencies: 2

**44. Add inline code documentation**
   - Write docstrings for all functions
   - Add inline comments explaining complex logic
   - Use type hints for function signatures
   - **What You'll Learn**: Code documentation standards, type hints
   - Dependencies: All code files

**45. Set up local deployment instructions**
   - Document how to run locally: `streamlit run app.py`
   - Include troubleshooting section
   - Test on fresh virtual environment
   - **What You'll Learn**: Local deployment, environment setup
   - Dependencies: 41, 42

**46. Prepare for Streamlit Cloud deployment**
   - Create .streamlit/config.toml for theme
   - Test app behavior in cloud environment
   - Set up secrets management for any API keys (if added)
   - **What You'll Learn**: Cloud deployment, Streamlit Cloud platform
   - Dependencies: 33, 42

**47. Deploy to Streamlit Cloud**
   - Connect GitHub repo to Streamlit Cloud
   - Configure deployment settings
   - Test deployed app and share link
   - **What You'll Learn**: Continuous deployment, cloud hosting
   - Dependencies: 46

**48. Create demo video or GIF**
   - Record short demo showing key features
   - Add to README to showcase the app
   - Use screen recording tools
   - **What You'll Learn**: Project presentation, creating demos
   - Dependencies: 41

**49. Add analytics (optional)**
   - Track basic usage metrics (number of check-ins per day)
   - Display personal analytics dashboard
   - Keep all data local (privacy-first)
   - **What You'll Learn**: Analytics implementation, data privacy
   - Dependencies: 21

**50. Final polish and user feedback iteration**
   - Share with friends/family for testing
   - Collect feedback and prioritize improvements
   - Fix any usability issues discovered
   - Celebrate completion! 🎉
   - **What You'll Learn**: User testing, iteration based on feedback
   - Dependencies: 47

## Global Teaching Notes

### Why This Project?
Habit tracking is a perfect first project because:
- **Immediate utility**: You'll actually use it, which is motivating
- **Simple data model**: Just habits and dates, easy to understand
- **Gratifying visualizations**: Charts and streaks make progress visible
- **Natural feature progression**: Start simple, add features incrementally
- **Real-world patterns**: CRUD operations, persistence, state management are universal

### Key Learning Moments
1. **Streamlit's Reactive Model**: Understanding that Streamlit reruns your script on every interaction is crucial. This might feel strange at first, but session state solves it elegantly.

2. **Date Handling**: Working with dates is surprisingly tricky. You'll learn about timezones, date arithmetic, and comparison. This comes up in almost every app.

3. **Data Persistence**: Seeing your data saved and reloaded between sessions makes the app feel "real." This is your first taste of database-like operations.

4. **Visualization Power**: Adding a simple line chart or heatmap transforms raw data into insight. This skill transfers to data science, dashboards, and analytics work.

### Common Pitfalls to Avoid
- **Forgetting to save data**: Always call `save_habits()` after modifying the habit list
- **Not handling missing files**: Your app will crash if habits.json doesn't exist. Use try/except.
- **Timezone confusion**: Use `datetime.date.today()` consistently, not `datetime.now()` which includes time
- **Overcomplicating too early**: Start with the simplest version that works, then add features

### Extension Ideas (After Completing Phase 5)
- **Habit reminders**: Use Streamlit's experimental notification features or send emails
- **Social features**: Share habits with friends, compare streaks
- **AI insights**: Use OpenAI API to analyze habits and suggest improvements
- **Mobile version**: Wrap in a mobile app using tools like Streamlit's mobile support or React Native
- **Gamification**: Add levels, badges, and achievements for maintaining streaks

### Development Workflow
1. **Always test as you go**: Run `streamlit run app.py` after each step to see changes
2. **Use git commits**: Commit after each phase so you can roll back if needed
3. **Read error messages**: Streamlit shows errors clearly in the browser - they're your friends
4. **Explore Streamlit docs**: The official docs have great examples for every widget

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Basic familiarity with command line

### Installation Steps

1. **Clone or download this project**
   ```bash
   git clone <your-repo-url>
   cd habit-tracker-app
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

5. **Open in browser**
   - Streamlit will automatically open http://localhost:8501
   - If not, navigate to that URL manually

### Running Tests
```bash
pytest tests/
```

## Success Metrics

You'll know you've succeeded when:
- ✅ You can create, view, edit, and delete habits through the UI
- ✅ Daily check-ins persist between app sessions
- ✅ Streak calculations are accurate, including edge cases
- ✅ Charts and visualizations update in real-time
- ✅ The app is deployed and accessible from any device
- ✅ You understand Streamlit's reactive model and can explain it
- ✅ You've written unit tests that pass for core functions
- ✅ Friends or family are actually using your habit tracker!

## Next Steps After Completion

1. **Extend the feature set**: Add categories, reminders, or social features
2. **Learn backend frameworks**: Try rebuilding with FastAPI + React to compare
3. **Explore data science**: Use your habit data for ML predictions or analysis
4. **Build another Streamlit app**: Now you know the patterns, what else could you build?
5. **Contribute to open source**: Find Streamlit projects on GitHub and contribute

**Congratulations on building your first web app!** This project gave you a foundation in web development, data persistence, visualization, and user experience design. These skills transfer to almost every software project you'll build in the future.
