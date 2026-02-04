# 🔍 GitHub Repo Agent

**Deep code analysis. Zero API keys. Instant insights.**

```
https://github.com/owner/repo → 10 seconds → 📊 full analysis
```

[![Deploy on Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yksanjo/github-repo-agent)
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/github-repo-agent)
[![Run on Replit](https://replit.com/badge/github/yksanjo/github-repo-agent)](https://replit.com/github/yksanjo/github-repo-agent)

[🚀 Live Demo](https://repo-agent-demo.vercel.app) · [📖 API Docs](#api) · [💬 Discord](https://discord.gg/repo-agent)

---

## What This Does

Paste any GitHub repo URL → Get instant analysis:

```
📊 Repository Analysis: vercel/next.js
======================================================================

📝 Languages:
   • TypeScript: 89.2%
   • Rust: 7.3%
   • JavaScript: 3.5%

🏗️  Structure:
   • Has README: ✅
   • Has LICENSE: ✅
   • Has CI/CD: ✅
   • Has Tests: ✅

🎯 Patterns: React, Turborepo, Docker, Testing, CI/CD

💡 Quick Wins:
   1. Update dependencies (12 behind)
   2. Add CodeQL security scanning
   3. Enable branch protection rules
```

**🎬 Demo:**
![demo](https://i.imgur.com/repo-agent-demo.gif)

---

## Copy-Paste Installation

### Option 1: One-Click Deploy (30 seconds)

Click a button above ↑

### Option 2: Local (3 commands)

```bash
git clone https://github.com/yksanjo/github-repo-agent.git
cd github-repo-agent && pip install -r requirements.txt
python web_server.py  # http://localhost:5001
```

### Option 3: Docker

```bash
docker run -p 5001:5001 yksanjo/github-repo-agent
```

---

## Usage

### Web Interface

```bash
python web_server.py
# Open http://localhost:5001
# Paste any GitHub repo URL
```

### CLI

```bash
# Analyze any public repo
python cli.py analyze vercel/next.js

# Get recommendations
python cli.py recommend owner/repo --focus security

# Export to JSON
python cli.py analyze owner/repo --export analysis.json
```

### Python API

```python
from github_repo_agent import GitHubRepoAgent

agent = GitHubRepoAgent()
analysis = agent.analyze_repo("vercel/next.js")
print(analysis['patterns'])  # ['React', 'Turborepo', 'Docker']
```

### MCP Server (for AI agents)

Add to `~/.mcp.json`:

```json
{
  "mcpServers": {
    "github-repo-agent": {
      "command": "python",
      "args": ["/path/to/github-repo-agent/mcp_server.py"]
    }
  }
}
```

Then ask Claude:
- `"Analyze facebook/react and tell me the architecture"`
- `"What security issues does this repo have?"`
- `"Compare next.js and remix-run/remix"`

---

## API {#api}

### `analyze_repo`

```json
{
  "owner": "vercel",
  "repo": "next.js"
}
```

Returns:
```json
{
  "languages": {"TypeScript": 89.2, "Rust": 7.3},
  "structure": {"has_readme": true, "has_ci_cd": true},
  "patterns": ["React", "Turborepo", "Docker"],
  "metrics": {"total_files": 4523, "test_files": 892}
}
```

### `get_recommendations`

```json
{
  "owner": "vercel",
  "repo": "next.js",
  "focus": "security"
}
```

### `compare_repos`

```json
{
  "repos": ["vercel/next.js", "remix-run/remix"]
}
```

---

## Pricing

| Tier | Cost | Usage |
|------|------|-------|
| Free | $0 | 100 repos/day |
| Pro | $0.01/repo | Unlimited + private repos |
| Enterprise | Custom | Self-hosted + SLA |

**For CI/CD Integration:**
```bash
curl -X POST https://api.repo-agent.io/analyze \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"repo": "owner/repo"}'
```

---

## Why This Exists

> "I wanted to understand codebases quickly without cloning and digging through files."

GitHub Repo Agent is **public infrastructure** for code analysis. It runs entirely locally (no API keys) or as a hosted service. AI agents use it to understand repositories before making changes.

---

## Features

- ✅ **Zero config** - Works out of the box
- ✅ **No API keys** - Analyzes public repos without authentication
- ✅ **Private repo support** - Add GitHub token for private repos
- ✅ **MCP integration** - Use with Claude/Cursor/Windsurf
- ✅ **CI/CD ready** - GitHub Actions integration
- ✅ **Export formats** - JSON, CSV, Markdown

---

## Metrics

![GitHub stars](https://img.shields.io/github/stars/yksanjo/github-repo-agent)
![Repos analyzed](https://img.shields.io/badge/repos%20analyzed-50K+-blue)
![Avg analysis time](https://img.shields.io/badge/avg%20time-8s-green)

---

## License

MIT - Analyze all the things.

Built by [@yksanjo](https://twitter.com/yksanjo) for developers who want to understand code fast.
