# Quick Start Guide

## Installation

```bash
cd github-repo-agent
pip install -r requirements.txt
```

## Basic Usage

### 1. Analyze any GitHub repository:

```bash
python cli.py analyze facebook/react
```

### 2. Get recommendations:

```bash
python cli.py recommend facebook/react
```

### 3. Get focused recommendations:

```bash
python cli.py recommend facebook/react --focus security
```

### 4. Get improvement plan:

```bash
python cli.py improve facebook/react
```

### 5. Export analysis:

```bash
python cli.py analyze facebook/react --export my_analysis.json
```

## Python API Usage

```python
from github_repo_agent import GitHubRepoAgent

# Initialize
agent = GitHubRepoAgent()

# Analyze
analysis = agent.analyze_repo("owner/repo")

# Get recommendations
recommendations = agent.get_recommendations("owner/repo")

# Get improvement plan
improvements = agent.suggest_improvements("owner/repo")
```

## Using with Private Repositories

Set your GitHub token:

```bash
export GITHUB_TOKEN=your_token_here
```

Or pass it directly:

```bash
python cli.py analyze owner/private-repo --token your_token_here
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [example.py](example.py) for more usage examples
- Customize the agent by extending the analyzer and recommender classes

