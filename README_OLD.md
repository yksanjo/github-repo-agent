# GitHub Repository Analysis Agent

An intelligent agent that deeply understands your GitHub repositories and provides actionable recommendations for improvement, security, performance, and best practices.

## Features

🔍 **Comprehensive Analysis**
- Repository structure analysis
- Language detection and distribution
- Dependency extraction and analysis
- Pattern identification (MVC, REST API, Docker, etc.)
- Codebase metrics (file sizes, test coverage, etc.)

💡 **Smart Recommendations**
- Security best practices
- Code quality improvements
- Performance optimizations
- Documentation enhancements
- Testing strategies
- CI/CD setup suggestions

📊 **Detailed Insights**
- Export analysis to JSON
- Priority-based recommendations
- Focused recommendations by area
- Improvement plans with quick wins

## 🚀 Quick Start (No API Keys Needed!)

The agent runs **entirely locally** - no external API keys required!

### Option 1: Quick Start Script
```bash
./quick_start.sh
```

### Option 2: Manual Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Launch the web interface:
```bash
python web_server.py
# Then open http://localhost:5001 in your browser
```

Or use the CLI:
```bash
python cli.py analyze owner/repo
```

**See [LAUNCH.md](LAUNCH.md) for detailed launch instructions.**

## 🖥️ Web Interface

The GitHub Repo Agent features a beautiful, modern web interface that provides comprehensive repository analysis at a glance:

### Interface Overview

**Header Section:**
- Clean, gradient header with the application title and rocket icon
- Subtitle: "Analyze any GitHub repository and get intelligent recommendations - No API keys needed!"

**Input Section:**
- Simple, intuitive input field for repository URLs
- Accepts both formats: `owner/repo` or full GitHub URLs
- One-click "Analyze Repository" button with magnifying glass icon

**Analysis Results Display:**

1. **📊 Overview Section**
   - Repository name and clickable GitHub URL
   - Quick reference to the analyzed repository

2. **📝 Languages Section**
   - Visual language distribution with percentage badges
   - Color-coded tags showing each language's contribution
   - Example: `python: 97.6%`, `html: 2.4%`

3. **🏗️ Structure Section**
   - Repository component indicators with status badges:
     - ✅ **README** (green) - Documentation present
     - ⚠️ **LICENSE** (orange) - License file status
     - ✅ **CI/CD** (blue) - Continuous integration setup
     - ✅ **Tests** (green) - Test directory presence

4. **🎯 Patterns Section**
   - Technology and architecture patterns detected:
     - REST API, MVC, Docker, Flask, Django
     - Testing frameworks, CI/CD patterns
     - All displayed as informative blue badges

5. **💡 Recommendations Section**
   - Priority-based actionable recommendations
   - Each recommendation includes:
     - **Title**: Clear action item (e.g., "Add a LICENSE file")
     - **Category**: Legal, CI/CD, Code Quality, Testing, Security
     - **Action**: Specific steps to implement
     - **Priority indicators**: Color-coded by importance
   - Examples:
     - Add LICENSE file (Legal category)
     - Set up Continuous Integration (CI/CD category)
     - Add type hints (Code Quality category)
     - Increase test coverage (Testing category)
     - Security scanning integration (Security category)

6. **🤖 AI Insights Section**
   - Architecture assessment with maturity level
   - Next steps for improvement
   - Intelligent analysis of codebase quality

### Design Features

- **Modern UI**: Clean white background with purple/blue gradient accents
- **Responsive Design**: Works on desktop and mobile devices
- **Color-Coded Status**: Visual indicators for quick scanning
- **Organized Layout**: Information grouped logically for easy reading
- **No Authentication Required**: Public repositories can be analyzed instantly

3. (Optional) Set up GitHub token for private repositories:
```bash
export GITHUB_TOKEN=your_github_token_here
```

## Usage

### Command Line Interface

#### Analyze a Repository
Get a comprehensive analysis of any GitHub repository:

```bash
python cli.py analyze owner/repo
```

Or with a full URL:
```bash
python cli.py analyze https://github.com/owner/repo
```

#### Get Recommendations
Get actionable recommendations for a repository:

```bash
python cli.py recommend owner/repo
```

Focus on specific areas:
```bash
python cli.py recommend owner/repo --focus security
python cli.py recommend owner/repo --focus performance
python cli.py recommend owner/repo --focus testing
```

#### Get Improvement Plan
Get a prioritized improvement plan:

```bash
python cli.py improve owner/repo
```

#### Export Analysis
Export analysis results to JSON:

```bash
python cli.py analyze owner/repo --export analysis.json
```

### Python API

You can also use the agent programmatically:

```python
from github_repo_agent import GitHubRepoAgent

# Initialize agent
agent = GitHubRepoAgent(github_token="your_token_here")  # Optional

# Analyze a repository
analysis = agent.analyze_repo("owner/repo")

# Get recommendations
recommendations = agent.get_recommendations("owner/repo", focus_area="security")

# Get improvement plan
improvements = agent.suggest_improvements("owner/repo")

# Export analysis
agent.export_analysis(analysis, "analysis.json")
```

## What the Agent Analyzes

### Repository Structure
- README presence and quality
- LICENSE file
- CI/CD configuration
- Test directories
- Documentation structure

### Languages & Dependencies
- Programming languages used
- Language distribution percentages
- Dependency files (package.json, requirements.txt, etc.)
- Dependency count and analysis

### Patterns & Architecture
- MVC patterns
- REST API structure
- Microservices architecture
- Containerization (Docker)
- Kubernetes deployments
- Framework detection (React, Vue, Django, Flask, etc.)

### Code Metrics
- Total files and code files
- Lines of code
- Average file size
- Test file ratio
- Code complexity indicators

### Recommendations Generated
- **Security**: Dependency updates, security scanning, best practices
- **Code Quality**: Refactoring suggestions, type hints, code organization
- **Testing**: Test coverage, testing frameworks, test structure
- **Documentation**: README improvements, API docs, guides
- **Performance**: Bundle optimization, code splitting, caching
- **DevOps**: CI/CD setup, containerization, deployment strategies

## Example Output

```
📊 Repository Analysis: owner/repo
======================================================================

🔗 URL: https://github.com/owner/repo
⏰ Analyzed at: 2024-01-15T10:30:00

📝 Languages Detected:
   • python: 75.5%
   • javascript: 20.3%
   • html: 4.2%

🏗️  Repository Structure:
   • Has README: ✅
   • Has LICENSE: ❌
   • Has CI/CD: ✅
   • Has Tests: ✅
   • Has Docs: ✅

🎯 Patterns Identified:
   • REST API
   • Docker
   • Testing
   • CI/CD

📈 Codebase Metrics:
   • Total Files: 245
   • Code Files: 180
   • Test Files: 45
   • Total Lines: 12,450
   • Avg File Size: 69.2 lines

💡 Recommendations:
----------------------------------------------------------------------

🔴 High Priority:
   1. Add a LICENSE file
      Category: Legal
      A license clarifies how others can use your code.
      Action: Choose an appropriate license (MIT, Apache 2.0, GPL, etc.)...
      Effort: Low
```

## Configuration

### GitHub Token
For private repositories or higher rate limits, set your GitHub token:

```bash
export GITHUB_TOKEN=your_token_here
```

Or pass it via command line:
```bash
python cli.py analyze owner/repo --token your_token_here
```

### Cache Directory
Repositories are cloned to `.repo_cache` by default. You can change this when initializing the agent:

```python
agent = GitHubRepoAgent(cache_dir="custom_cache_dir")
```

## Extending the Agent

The agent is designed to be extensible. You can:

1. **Add custom analyzers**: Extend `CodeAnalyzer` class
2. **Custom recommendations**: Extend `Recommender` class
3. **Additional data sources**: Extend `GitHubClient` class
4. **New output formats**: Add export methods to `GitHubRepoAgent`

## Development

### Project Structure
```
github-repo-agent/
├── github_repo_agent/
│   ├── __init__.py
│   ├── agent.py          # Main agent class
│   ├── github_client.py  # GitHub API client
│   ├── code_analyzer.py  # Code analysis logic
│   └── recommender.py    # Recommendation engine
├── cli.py                # Command-line interface
├── requirements.txt      # Dependencies
└── README.md            # This file
```

## Future Enhancements

- [ ] AI-powered code understanding using LLMs
- [ ] Automated code generation for recommendations
- [ ] Integration with code quality tools (SonarQube, CodeClimate)
- [ ] Support for multiple repositories comparison
- [ ] Historical analysis and trend tracking
- [x] Web dashboard interface ✅
- [ ] Slack/Teams integration for notifications
- [ ] Automated PR creation for quick wins

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this project for your own repositories!

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Made with ❤️ for developers who want to improve their codebases**

