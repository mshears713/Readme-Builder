Project Forge is a small, focused multi-agent system built with CrewAI that does the job you and ChatGPT have been doing by hand:
	•	Take a vague project idea you type on the CLI
	•	Clean and expand it
	•	Extract learning and technical goals
	•	Choose appropriate frameworks and tools for your skill level
	•	Design a 5-phase, 50-step build plan
	•	Enrich it with teaching commentary (what you’ll learn and why)
	•	Evaluate and refine the plan
	•	Output a single, extensive README/PRD file that you can feed to Claude Code or another code LLM to build the actual project

This meta-system is small enough to get running quickly, but structured enough to scale to many future projects.

⸻

	1.	TEACHING GOALS

⸻

PRIMARY LEARNING GOALS:
	•	Understand how to structure a practical multi-agent system using CrewAI
	•	See clear separations of concern between different reasoning flows
	•	Learn how to encode learning objectives directly into project specs
	•	Learn how to connect CLI input → agents → final artifact

SECONDARY LEARNING GOALS:
	•	Data modeling for project plans (phases, steps, goals)
	•	Evaluation patterns (self-checking agents)
	•	Framework selection logic based on constraints (skill, time, complexity)
	•	How to design “meta-tools” that generate READMEs/PRDs

⸻

	2.	HIGH-LEVEL ARCHITECTURE (ASCII)
                ┌─────────────────────────┐
                │       CLI Input         │
                │  (raw project idea)     │
                └───────────┬─────────────┘
                            │
                 ┌──────────▼───────────┐
                 │  ConceptExpander     │
                 └──────────┬───────────┘
                            │ refined concept
                 ┌──────────▼───────────┐
                 │   GoalsAnalyzer      │
                 └──────────┬───────────┘
                            │ goals
                 ┌──────────▼───────────┐
                 │ FrameworkSelector    │
                 └──────────┬───────────┘
                            │ stack choice
                 ┌──────────▼───────────┐
                 │   PhaseDesigner      │
                 └──────────┬───────────┘
                            │ 5 phases × 50 steps
                 ┌──────────▼───────────┐
                 │     TeacherAgent     │
                 └──────────┬───────────┘
                            │ teaching annotations
                 ┌──────────▼───────────┐
                 │    EvaluatorAgent    │
                 └──────────┬───────────┘
                            │ approved plan
                 ┌──────────▼───────────┐
                 │   PRD/READMEWriter   │
                 └──────────┬───────────┘
                            │
                ┌──────────▼────────────┐
                │   Final README/PRD    │
                └───────────────────────┘CrewAI orchestrates these agents into a single “crew” that runs end-to-end when you call the CLI entrypoint.

⸻

	3.	DIRECTORY STRUCTURE

⸻

project_forge/
src/
agents/
concept_expander_agent.py
goals_analyzer_agent.py
framework_selector_agent.py
phase_designer_agent.py
teacher_agent.py
evaluator_agent.py
prd_writer_agent.py
tools/
text_cleaner_tool.py
rubric_tool.py
consistency_tool.py
models/
project_models.py   # ProjectIdea, Goals, Phase, Step, Plan
orchestration/
crew_config.py      # Crew + Tasks + wiring
runner.py           # CLI entrypoint logic
config/
defaults.yaml       # default options, skill presets, templates
examples/
example_input_ideas.txt
example_generated_readmes/
README.md

⸻

	4.	AGENT ROLES

⸻

ConceptExpanderAgent
	•	Input: raw idea string
	•	Output: structured ProjectIdea (domain, scale, constraints, vibe)
	•	Responsible for: removing noise, clarifying, expanding context

GoalsAnalyzerAgent
	•	Input: refined ProjectIdea
	•	Output: explicit learning goals + technical goals
	•	Responsible for: extracting what you should learn, what tech to practice

FrameworkSelectorAgent
	•	Input: ProjectIdea + goals + your skill profile
	•	Output: recommended stack (e.g., Streamlit vs FastAPI, SQLite vs Postgres)
	•	Responsible for: choosing frameworks that are simple and appropriate

PhaseDesignerAgent
	•	Input: all of the above
	•	Output: 5 phases × 10 steps (small, digestible, realistic)
	•	Responsible for: turning concept into structured build plan

TeacherAgent
	•	Input: the plan (phases + steps) and goals
	•	Output: enriched plan with “what you’ll learn,” hints, and teaching notes per phase/step
	•	Responsible for: shaping each phase/step as a mini lesson

EvaluatorAgent
	•	Input: enriched plan and metadata
	•	Output: either “approve + small fixes” or “request revisions” messages consumed by other agents
	•	Responsible for: sanity-checking structure, coherence, balance

PRDWriterAgent
	•	Input: final approved plan + framework choices + goals
	•	Output: single README/PRD text (this is what you’ll feed to Claude Code)
	•	Responsible for: turning structured plan into a narrative, detailed, buildable document

⸻

	5.	DATA MODEL (MODELS)

⸻

Core objects in models/project_models.py:
	•	ProjectIdea
	•	raw_description
	•	refined_summary
	•	constraints (time, complexity, hardware, etc.)
	•	ProjectGoals
	•	learning_goals (list of strings)
	•	technical_goals (list of strings)
	•	priority_notes
	•	FrameworkChoice
	•	frontend (e.g., Streamlit / None)
	•	backend (FastAPI / CLI-only / etc.)
	•	storage (SQLite / files)
	•	special_libs (CrewAI, LangChain, etc.)
	•	Phase
	•	index
	•	name
	•	description
	•	steps: List[Step]
	•	Step
	•	index
	•	title
	•	description
	•	what_you_learn
	•	dependencies
	•	ProjectPlan
	•	idea
	•	goals
	•	framework
	•	phases
	•	teaching_notes (global)

All agents read and write these models, so the system remains structured.

⸻

	6.	CLI FLOW

⸻

CLI entrypoint (runner.py) should:
	1.	Accept a single string argument for the idea, or read from stdin.
	2.	Initialize the CrewAI crew with all agents and tools.
	3.	Run the crew to completion:
	•	Concept expansion
	•	Goals analysis
	•	Framework selection
	•	Phase design
	•	Teaching enrichment
	•	Evaluation and refinement
	•	PRD/README writing
	4.	Write the final README/PRD to disk (output/PROJECT_NAME_README.md).
	5.	Print a short summary to stdout.

Example invocation:

python -m src.orchestration.runner “Build an async wildfire grant dashboard that teaches me Streamlit and async scraping”

⸻

	7.	PHASES + STEPS (5 PHASES × 10 STEPS)

⸻

Claude Code: do not modify this README after Phase 1.
Implement exactly these phases and steps.
Keep steps small and realistic.
All Python files must include narrative header docstrings and inline teaching comments.

────────────────────────────────────────────
PHASE 1 — FOUNDATIONS & MODELS (10 STEPS)
────────────────────────────────────────────
	1.	Create base directory structure as defined above.
	2.	Implement project_models.py with empty dataclasses for core objects.
	3.	Fill dataclasses with fields for ProjectIdea, ProjectGoals, FrameworkChoice, Phase, Step, ProjectPlan.
	4.	Add docstrings explaining purpose of each model and how agents use them.
	5.	Implement text_cleaner_tool.py with simple normalization utilities.
	6.	Implement rubric_tool.py with a basic evaluation rubric structure (clarity, feasibility, teaching value).
	7.	Implement consistency_tool.py stub for later cross-checks.
	8.	Add config/defaults.yaml with placeholders for skill presets and framework templates.
	9.	Create crew_config.py with stubs for agents and tasks (no real logic yet).
	10.	Create runner.py with placeholder CLI that just prints the raw idea.

────────────────────────────────────────────
PHASE 2 — CORE AGENTS (10 STEPS)
────────────────────────────────────────────
11. Implement ConceptExpanderAgent class file with CrewAI Agent definition.
12. Implement basic logic to clean and expand the raw idea into ProjectIdea.
13. Implement GoalsAnalyzerAgent with prompts focused on learning + technical goals.
14. Implement FrameworkSelectorAgent with prompts that consider simplicity, your skills, and common stacks (Streamlit, FastAPI, SQLite, etc.).
15. Wire these three agents into crew_config.py as part of a first “planning crew.”
16. Implement a simple Task flow to: idea → concept → goals → frameworks.
17. Update runner.py to run the planning crew and print intermediate objects.
18. Add inline comments and header docstrings explaining each agent’s role.
19. Use rubric_tool in a basic way to score the clarity of the refined concept.
20. Verify via CLI that Phase 2 runs end-to-end and produces a refined summary and framework choice.

────────────────────────────────────────────
PHASE 3 — PLAN DESIGN & TEACHING (10 STEPS)
────────────────────────────────────────────
21. Implement PhaseDesignerAgent to build 5 phases × 10 steps from idea + goals + frameworks.
22. Encode rules to keep steps small, concrete, and buildable.
23. Implement TeacherAgent to add “what you’ll learn” fields to phases and steps.
24. Add global teaching notes to ProjectPlan (overall pedagogical arc).
25. Extend rubric_tool to check balance of phases (no empty or overloaded phases).
26. Implement EvaluatorAgent with modes: concept_eval, goals_eval, plan_eval.
27. Wire PhaseDesignerAgent, TeacherAgent, and EvaluatorAgent into crew_config.py as a second stage of the crew.
28. Update runner.py to execute both the planning stage and the planning+teaching stage.
29. Add consistency_tool usage to ensure phase counts and step counts match expectations.
30. Test via CLI: confirm a full plan object (ProjectPlan) is produced and evaluated.

────────────────────────────────────────────
PHASE 4 — PRD/README WRITING & OUTPUT (10 STEPS)
────────────────────────────────────────────
31. Implement PRDWriterAgent to convert ProjectPlan into a single README/PRD text.
32. Define a standard structure for all generated READMEs (Overview, Goals, Architecture, Phases, Steps, Frameworks, Notes).
33. Ensure TeacherAgent’s learning notes are embedded per phase/step in the README.
34. Ensure EvaluatorAgent can suggest small fixes and send updated instructions to PhaseDesigner or TeacherAgent.
35. Add logic in crew_config.py to perform evaluation and rewrites until a simple “good enough” threshold is met.
36. Update runner.py to write the README/PRD output to disk in an output/ directory.
37. Add logging to show which agents ran and what decisions were made.
38. Add basic error handling around API calls and missing config.
39. Add narrative docstrings to PRDWriterAgent that explain how to modify templates later.
40. Test full CLI flow: idea → README file appears in output.

────────────────────────────────────────────
PHASE 5 — POLISH, PRESETS, AND EXAMPLES (10 STEPS)
────────────────────────────────────────────
41. Add skill-level presets to defaults.yaml (e.g., beginner, intermediate, advanced) and teach FrameworkSelectorAgent to use them.
42. Add example input ideas to examples/example_input_ideas.txt.
43. Generate 2–3 example READMEs and store in examples/example_generated_readmes/.
44. Add command-line flags to runner.py for skill level and project type (toy, medium, ambitious).
45. Improve rubric_tool to rate teaching clarity, technical depth, and feasibility.
46. Improve EvaluatorAgent to reject plans that are too big for “one week” or too trivial.
47. Add developer notes to README about how to add new agents or tools later.
48. Add minimal test file to validate basic model integrity and crew wiring.
49. Clean up inline comments and ensure all modules have clear header docstrings.
50. Run an end-to-end dry run with several different idea prompts and adjust defaults.yaml for better behavior.

⸻

	8.	IMPLEMENTATION RULES FOR CLAUDE CODE

⸻

	•	Do not modify this README after Phase 1.
	•	Implement each phase in order when instructed.
	•	Keep agent implementations small and clear, with teaching docstrings.
	•	Use CrewAI idioms for defining agents, tasks, and crews.
	•	Favor readability over cleverness.
	•	Ensure runner.py always remains the single entrypoint.
	•	Keep configuration editable via defaults.yaml and not buried in code.

⸻

	9.	SETUP

⸻

	•	Python 3.11+ recommended
	•	pip install crewai (or appropriate package name) and OpenAI client
	•	Use a .env file or environment variables for OPENAI_API_KEY

Example:

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.orchestration.runner “Build a Streamlit teaching app for async APIs”
