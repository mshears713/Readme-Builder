# Multi-Agent Code Review System with CrewAI

## Overview

An advanced multi-agent system that performs automated, comprehensive code reviews using CrewAI and multiple specialized AI agents. This system analyzes pull requests or code directories, provides detailed feedback on code quality, security, performance, and best practices, and generates actionable improvement suggestions.

The system orchestrates multiple AI agents, each with specialized expertise:
- **AnalyzerAgent**: Performs static analysis and identifies code smells
- **SecurityAgent**: Scans for vulnerabilities and security anti-patterns
- **PerformanceAgent**: Identifies performance bottlenecks and optimization opportunities
- **StyleAgent**: Enforces coding standards and best practices
- **DocumentationAgent**: Reviews and suggests documentation improvements
- **SynthesisAgent**: Combines findings into a comprehensive review report

This advanced project teaches multi-agent architectures, LLM integration, static analysis, CI/CD integration, and building production-grade developer tools.

## Teaching Goals

### Learning Goals
- **Multi-Agent Systems**: Design and orchestrate multiple AI agents with CrewAI
- **LLM Integration**: Effectively prompt and coordinate LLMs for specialized tasks
- **Static Analysis**: Leverage AST parsing and linting tools programmatically
- **GitHub API**: Interact with GitHub for PR analysis and commenting
- **Async Programming**: Handle concurrent agent execution efficiently
- **Agent Communication**: Implement inter-agent communication and data sharing

### Technical Goals
- Build a production-quality developer tool that provides value
- Implement sophisticated prompt engineering for specialized agents
- Integrate multiple code analysis tools (pylint, bandit, radon, etc.)
- Create a plugin architecture for extensibility
- Deploy as GitHub Action and CLI tool
- Handle real-world edge cases (large codebases, multiple languages)

### Priority Notes
This project is for experienced developers ready to tackle production-complexity systems. You'll learn to combine traditional static analysis tools with modern LLMs, creating a hybrid system that's more powerful than either alone. The focus is on architecture, prompt engineering, and building tools that developers actually want to use.

## Technology Stack

**Agent Framework**: CrewAI
- Orchestrates multiple specialized agents
- Handles task delegation and result aggregation
- Built-in memory and context management

**LLM Provider**: OpenAI GPT-4 (configurable for other providers)
- GPT-4 for synthesis and complex reasoning
- GPT-3.5-turbo for routine analysis tasks
- Support for local models via LiteLLM

**Static Analysis Tools**:
- `pylint`: Comprehensive Python linting
- `bandit`: Security vulnerability scanner
- `radon`: Complexity and maintainability metrics
- `mypy`: Type checking
- `black`: Code formatting verification
- `isort`: Import organization
- `ast`: Python abstract syntax tree parsing

**Integrations**:
- `PyGithub`: GitHub API client for PR analysis
- `click`: CLI framework
- `pydantic`: Configuration and data validation
- `redis`: Agent state and result caching
- `pytest` + `pytest-asyncio`: Async testing

**Deployment**:
- GitHub Actions for CI/CD integration
- Docker for containerized deployment
- FastAPI for optional web interface

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                   Input Layer                                │
│  - GitHub PR webhook                                         │
│  - CLI command (local directory)                             │
│  - API request (web interface)                               │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                Orchestrator (CrewAI Crew)                    │
│  - Parses codebase structure                                 │
│  - Delegates tasks to specialized agents                     │
│  - Manages agent communication and shared context            │
└─────┬───────┬────────┬────────┬──────────┬─────────┬────────┘
      │       │        │        │          │         │
      ▼       ▼        ▼        ▼          ▼         ▼
┌──────────┐┌─────────┐┌───────┐┌──────────┐┌────────┐┌────────┐
│Analyzer  ││Security ││Perform││Style     ││Docs    ││Synth   │
│Agent     ││Agent    ││Agent  ││Agent     ││Agent   ││Agent   │
└────┬─────┘└────┬────┘└───┬───┘└────┬─────┘└───┬────┘└───┬────┘
     │           │          │         │          │         │
     │   ┌───────▼──────────▼─────────▼──────────▼─────┐   │
     │   │      Static Analysis Tools Layer            │   │
     │   │  pylint, bandit, radon, mypy, black         │   │
     │   └──────────────────┬──────────────────────────┘   │
     │                      │                              │
     └──────────────────────▼──────────────────────────────┘
                            │
                            ▼
           ┌────────────────────────────────────┐
           │     Synthesis & Report Generation   │
           │  - Aggregate findings               │
           │  - Prioritize issues                │
           │  - Generate actionable suggestions  │
           └────────────┬───────────────────────┘
                        │
                        ▼
           ┌────────────────────────────────────┐
           │         Output Layer                │
           │  - Markdown report                  │
           │  - GitHub PR comment                │
           │  - JSON for CI/CD                   │
           │  - Slack/email notifications        │
           └─────────────────────────────────────┘
```

## Implementation Plan

### Phase 1: Core Architecture & Code Analysis Foundation (10 steps)

**1. Design multi-agent system architecture**
- Define agent roles and responsibilities
- Design inter-agent communication protocol
- Plan data flow and shared context strategy
- **What You'll Learn**: System architecture, agent design patterns

**2. Set up project structure with modular agent design**
- Create agents/, tools/, models/, orchestration/ directories
- Implement base agent classes and interfaces
- Set up configuration management
- **What You'll Learn**: Advanced Python project organization, abstractions

**3. Implement AST parser for Python code structure analysis**
- Parse Python files into abstract syntax trees
- Extract classes, functions, imports, complexity metrics
- Build code navigation utilities
- **What You'll Learn**: AST manipulation, compiler basics, metaprogramming

**4. Integrate pylint for code quality analysis**
- Run pylint programmatically on code files
- Parse pylint output into structured data
- Categorize issues by severity and type
- **What You'll Learn**: Linting tools, subprocess management, parsing

**5. Integrate bandit for security scanning**
- Run bandit security scanner
- Identify common vulnerabilities (SQL injection, hardcoded secrets, etc.)
- Prioritize security issues by risk level
- **What You'll Learn**: Security analysis, vulnerability detection, secure coding

**6. Integrate radon for complexity metrics**
- Calculate cyclomatic complexity
- Measure maintainability index
- Identify overly complex functions
- **What You'll Learn**: Code metrics, complexity theory, maintainability

**7. Create unified analysis result data model**
- Define Pydantic models for Analysis Result, Issue, Suggestion
- Standardize output from different analysis tools
- Implement severity scoring system
- **What You'll Learn**: Data modeling, normalization, schema design

**8. Implement file filtering and ignore patterns**
- Respect .gitignore and custom ignore patterns
- Filter by file types, directories, size limits
- Handle binary files and generated code
- **What You'll Learn**: File system operations, glob patterns, filtering

**9. Build code snippet extraction utility**
- Extract relevant code context for issues
- Include surrounding lines for context
- Syntax highlight snippets for reports
- **What You'll Learn**: Text processing, context extraction

**10. Create comprehensive test suite for analysis tools**
- Test AST parsing with various code patterns
- Test tool integrations with sample code
- Test error handling for malformed code
- **What You'll Learn**: Testing complex systems, fixture design

### Phase 2: Specialized Agent Implementation (10 steps)

**11. Implement AnalyzerAgent with CrewAI**
- Define agent role and goal for code analysis
- Create prompts for identifying code smells
- Integrate with static analysis tools
- **What You'll Learn**: CrewAI agent creation, prompt engineering basics

**12. Implement SecurityAgent for vulnerability detection**
- Define security-focused agent persona
- Integrate bandit results with LLM analysis
- Identify security anti-patterns beyond tool capabilities
- **What You'll Learn**: Security-focused prompting, vulnerability assessment

**13. Implement PerformanceAgent for optimization suggestions**
- Analyze algorithmic complexity
- Identify common performance anti-patterns
- Suggest optimization strategies with examples
- **What You'll Learn**: Performance analysis, algorithmic thinking

**14. Implement StyleAgent for coding standards**
- Enforce PEP 8 and project-specific style guides
- Check naming conventions, docstring standards
- Verify import organization and file structure
- **What You'll Learn**: Style guides, code consistency, linting

**15. Implement DocumentationAgent for docs quality**
- Review docstring completeness and quality
- Check README and inline comment coverage
- Suggest documentation improvements
- **What You'll Learn**: Documentation standards, technical writing

**16. Implement SynthesisAgent for report aggregation**
- Collect findings from all specialized agents
- Prioritize issues by impact and effort
- Generate executive summary and action items
- **What You'll Learn**: Data aggregation, prioritization algorithms

**17. Design agent communication and shared context**
- Implement shared memory/context for agents
- Allow agents to build on each other's findings
- Handle agent dependencies and ordering
- **What You'll Learn**: Inter-agent communication, state management

**18. Implement sophisticated prompt engineering**
- Create few-shot examples for each agent
- Tune prompts for consistency and accuracy
- Handle context window limits efficiently
- **What You'll Learn**: Advanced prompt engineering, LLM limitations

**19. Add agent configuration and customization**
- Allow users to enable/disable specific agents
- Configure severity thresholds and rules
- Support custom analysis rules
- **What You'll Learn**: Plugin architecture, configuration management

**20. Build agent testing framework**
- Test each agent with known code samples
- Verify output consistency and quality
- Measure agent performance (tokens, time, accuracy)
- **What You'll Learn**: AI system testing, evaluation metrics

### Phase 3: GitHub Integration & PR Analysis (10 steps)

**21. Implement GitHub API client**
- Authenticate with GitHub (PAT or GitHub App)
- Fetch PR metadata, files, and diffs
- Handle API rate limiting gracefully
- **What You'll Learn**: REST API integration, authentication, rate limiting

**22. Parse PR diffs to identify changed code**
- Extract only modified/added code from diffs
- Map line numbers between diff and full file
- Focus analysis on PR changes, not entire codebase
- **What You'll Learn**: Diff parsing, change detection

**23. Analyze PR code against base branch**
- Compare complexity/quality metrics: before vs after
- Identify if PR improves or degrades code quality
- Calculate delta metrics for reporting
- **What You'll Learn**: Comparative analysis, metrics tracking

**24. Generate inline PR comments**
- Post comments at specific lines using GitHub API
- Link comments to specific issues found by agents
- Avoid duplicate comments on subsequent runs
- **What You'll Learn**: GitHub code review API, comment management

**25. Create comprehensive PR review summary**
- Generate top-level PR comment with full report
- Include metrics, issue counts, and recommendations
- Add visual elements (badges, charts) using markdown
- **What You'll Learn**: Markdown generation, data visualization in text

**26. Implement PR approval/request changes logic**
- Auto-approve PRs that meet quality threshold
- Request changes for PRs with critical issues
- Make threshold configurable
- **What You'll Learn**: Automated decision-making, configurable policies

**27. Handle large PRs efficiently**
- Paginate through large file lists
- Batch analysis to avoid timeouts
- Provide incremental feedback
- **What You'll Learn**: Performance optimization, pagination

**28. Add PR description analysis**
- Check if PR description is clear and complete
- Verify linked issues and breaking change notes
- Suggest improvements to PR documentation
- **What You'll Learn**: Natural language processing, heuristics

**29. Implement multi-language support detection**
- Detect languages in PR (Python, JS, Go, etc.)
- Route to appropriate analysis tools per language
- Provide graceful degradation for unsupported languages
- **What You'll Learn**: Polyglot analysis, extensibility

**30. Test GitHub integration with real PRs**
- Create test repository with sample PRs
- Verify all GitHub operations work correctly
- Test edge cases (empty PRs, binary files, huge PRs)
- **What You'll Learn**: Integration testing, test repositories

### Phase 4: CLI, Deployment & Advanced Features (10 steps)

**31. Build CLI with Click**
- Commands: analyze, review-pr, configure
- Support local directory analysis and GitHub PR URLs
- Pretty terminal output with rich or colorama
- **What You'll Learn**: CLI design, argument parsing, terminal UX

**32. Implement result caching with Redis**
- Cache analysis results to avoid re-analyzing unchanged code
- Invalidate cache on code changes
- Support TTL and manual cache clearing
- **What You'll Learn**: Caching strategies, Redis, performance optimization

**33. Add async execution for agent parallelization**
- Run independent agents concurrently
- Use asyncio for I/O-bound operations
- Maintain agent dependencies (e.g., Synthesis waits for others)
- **What You'll Learn**: Async programming, concurrency, dependency graphs

**34. Implement incremental analysis**
- Analyze only changed files, not entire codebase
- Track analysis state across runs
- Provide "full" vs "incremental" modes
- **What You'll Learn**: Incremental computation, state tracking

**35. Create GitHub Action for CI/CD integration**
- Package system as GitHub Action
- Configure action inputs (token, severity threshold, etc.)
- Handle Action-specific output formats
- **What You'll Learn**: GitHub Actions, CI/CD, automation

**36. Build FastAPI web interface (optional)**
- Dashboard showing recent reviews
- Webhook endpoint for GitHub events
- Real-time review progress via WebSockets
- **What You'll Learn**: Web backends, webhooks, real-time communication

**37. Implement configurable rule sets**
- Allow users to define custom rules in YAML
- Support rule severity overrides
- Create preset rule sets (strict, moderate, lenient)
- **What You'll Learn**: Rule engines, YAML configuration, presets

**38. Add support for JavaScript/TypeScript analysis**
- Integrate ESLint and TypeScript compiler
- Create JS-specific analysis agents
- Support monorepos with multiple languages
- **What You'll Learn**: Polyglot tooling, language-specific analysis

**39. Implement report formats (JSON, HTML, PDF)**
- Export review results in multiple formats
- Generate visual HTML reports with charts
- Support JSON for programmatic consumption
- **What You'll Learn**: Multi-format output, data serialization, templating

**40. Add Slack/email notifications**
- Send notifications when review completes
- Include summary and link to full report
- Support webhook integrations
- **What You'll Learn**: Notifications, integrations, webhooks

### Phase 5: Production Hardening & Advanced AI Features (10 steps)

**41. Implement robust error handling and retries**
- Retry LLM calls on transient failures
- Gracefully handle API errors (rate limits, timeouts)
- Continue analysis even if one agent fails
- **What You'll Learn**: Resilience patterns, error recovery

**42. Add comprehensive logging and observability**
- Structured logging (JSON format)
- Trace IDs for request tracking
- Integrate with observability platforms (optional)
- **What You'll Learn**: Production logging, observability, debugging

**43. Implement cost tracking for LLM usage**
- Track tokens used per agent and total
- Estimate costs based on pricing
- Provide budget limits and alerts
- **What You'll Learn**: LLM cost management, resource limits

**44. Optimize prompts for token efficiency**
- Reduce prompt sizes without sacrificing quality
- Use prompt caching where available
- Experiment with smaller models for routine tasks
- **What You'll Learn**: Prompt optimization, cost reduction

**45. Add agent learning from user feedback**
- Allow users to mark false positives
- Store feedback in database
- Use feedback to tune agent prompts (manual or automated)
- **What You'll Learn**: Feedback loops, continuous improvement

**46. Implement diff-aware analysis**
- Focus LLM analysis on code changes, not entire files
- Reduce context size for large files
- Improve relevance of findings
- **What You'll Learn**: Context optimization, diff analysis

**47. Create benchmarking suite**
- Curate set of test repositories with known issues
- Measure precision, recall, and F1 score
- Track performance over time
- **What You'll Learn**: AI evaluation, benchmarking, metrics

**48. Add support for private LLM models**
- Support self-hosted models via LiteLLM
- Allow enterprise users to avoid sending code to external APIs
- **What You'll Learn**: LLM hosting, privacy, enterprise features

**49. Dockerize and create deployment documentation**
- Create optimized Docker image
- Document deployment on various platforms
- Provide Kubernetes manifests (optional)
- **What You'll Learn**: Containerization, deployment, DevOps

**50. Conduct user testing and iterate**
- Deploy to beta users (internal team or open source community)
- Collect feedback on accuracy and usefulness
- Iterate on prompts and features based on real usage
- **What You'll Learn**: User feedback, iteration, product development

## Global Teaching Notes

### Why This Project?
Multi-agent code review systems represent the cutting edge of AI-assisted development:
- **Real-world impact**: Improves code quality and catches bugs automatically
- **Advanced AI**: Combines multiple LLMs with traditional tools for hybrid intelligence
- **System design**: Requires sophisticated architecture and coordination
- **Production complexity**: Must handle edge cases, large codebases, and real users

### Key Learning Moments

1. **Agent Orchestration**: Designing how multiple AI agents collaborate is fundamentally different from single-agent systems. You'll learn to balance independence (parallel execution) with dependencies (sequential when needed).

2. **Prompt Engineering**: Different agents need vastly different prompting strategies. The SecurityAgent needs to be paranoid and thorough; the SynthesisAgent needs to be concise and prioritize. Crafting these personas is an art.

3. **Hybrid AI Systems**: Pure LLMs miss issues that linters catch, and linters miss nuanced issues that LLMs understand. Combining both creates emergent capabilities neither has alone.

4. **Production AI**: Handling LLM failures, rate limits, cost management, and response variability is crucial for production AI systems. This project teaches you to build robust, reliable AI tools.

### Common Pitfalls

- **Context window overflow**: Large files exceed LLM context limits. Use chunking and summarization.
- **Over-prompting**: Verbose prompts waste tokens and money. Be concise and use few-shot examples.
- **Agent duplication**: Agents may identify the same issue. Implement deduplication logic.
- **False positives**: LLMs hallucinate issues that don't exist. Use confidence scoring and verification.
- **Cost explosion**: Running GPT-4 on every PR can get expensive fast. Use GPT-3.5 for routine tasks and cache aggressively.

### Extension Ideas

- **Auto-fixing**: Generate code patches to fix identified issues
- **Learning mode**: Fine-tune models on your codebase's patterns
- **Team analytics**: Track code quality trends across team over time
- **Review assignment**: Auto-assign PRs to best human reviewer based on expertise
- **Custom agents**: Allow users to define their own specialized agents

## Setup Instructions

### Prerequisites
- Python 3.10+
- OpenAI API key (or other LLM provider)
- GitHub Personal Access Token (for PR analysis)
- Redis (optional, for caching)

### Local Development

1. **Clone repository**
   ```bash
   git clone <repo-url>
   cd code-review-agent-system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Add OPENAI_API_KEY, GITHUB_TOKEN, etc.
   ```

4. **Run CLI analysis on local directory**
   ```bash
   python -m app.cli analyze ./path/to/code
   ```

5. **Analyze a GitHub PR**
   ```bash
   python -m app.cli review-pr https://github.com/owner/repo/pull/123
   ```

### GitHub Action Usage

```yaml
# .github/workflows/code-review.yml
name: AI Code Review
on: [pull_request]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: your-username/code-review-action@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          openai-api-key: ${{ secrets.OPENAI_API_KEY }}
          severity-threshold: medium
```

### Docker Deployment

```bash
docker build -t code-review-ai .
docker run -e OPENAI_API_KEY=sk-... code-review-ai analyze /code
```

## Success Metrics

✅ Successfully analyzes PRs with 10+ files in under 2 minutes
✅ Precision >70% (findings are actually issues)
✅ Recall >60% (catches majority of issues)
✅ Cost per PR review <$0.50
✅ Deployed as GitHub Action used by 5+ repositories
✅ Handles edge cases gracefully (no crashes on malformed code)
✅ Users report 50%+ of suggestions are adopted
✅ Agents execute in parallel for 2-3x speedup vs sequential

## Next Steps

1. **Open source**: Release on GitHub and build community
2. **SaaS version**: Build hosted service for teams without self-hosting
3. **Multi-repo insights**: Track quality trends across organization
4. **IDE integration**: VSCode extension for real-time review
5. **Fine-tuning**: Train custom models on your team's codebase

This project represents production-grade AI engineering, combining classical software engineering with modern LLM capabilities. The skills you develop here—agent orchestration, prompt engineering, system design—are highly valuable in the rapidly evolving AI landscape.
