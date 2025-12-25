# Local Setup Guide - GitHub Repo Agent

## ✅ Status: Working Locally!

Your GitHub Repo Agent is now running locally and working perfectly!

## 🚀 Quick Start

### Start the Server

```bash
cd /Users/yoshikondo/github-repo-agent
python3 web_server.py
```

The server will automatically find an available port (usually 5001) and display:
```
🚀 GitHub Repository Agent - Local Web Server
📍 Server starting at: http://localhost:5001
```

### Access the Web Interface

1. Open your browser
2. Navigate to: **http://localhost:5001**
3. Enter a repository URL (e.g., `facebook/react` or `https://github.com/facebook/react`)
4. Click "🔍 Analyze Repository"

### Test via API (Command Line)

```bash
# Test the API directly
curl -X POST http://localhost:5001/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "facebook/react"}'
```

## 📊 Verified Working Features

✅ Web interface loads correctly  
✅ API endpoint responds (`/api/analyze`)  
✅ Repository analysis works  
✅ AI insights generation  
✅ Recommendations generation  
✅ No GPU needed - runs entirely on CPU  

## 🔍 What It Analyzes

- Repository structure (README, LICENSE, CI/CD, tests)
- Programming languages and distribution
- Dependencies and package files
- Code patterns (React, Docker, REST API, etc.)
- Code metrics (files, lines of code, test coverage)
- Security recommendations
- Performance optimizations
- Documentation suggestions

## 🛠️ Troubleshooting

### Server Already Running?

If you see "Address already in use":
```bash
# Find and kill the existing process
lsof -ti:5001 | xargs kill -9

# Or use a different port
PORT=8080 python3 web_server.py
```

### Dependencies Missing?

```bash
pip3 install flask requests
```

### Check Server Status

```bash
curl http://localhost:5001/api/health
```

Should return: `{"status": "ok", "message": "GitHub Repository Agent is running"}`

## 🌐 Vercel Deployment Issues

If your Vercel deployment isn't working, common issues:

1. **Environment Variables**: Make sure `GITHUB_TOKEN` is set in Vercel settings (optional, but helps with rate limits)
2. **Build Configuration**: Check `vercel.json` routing
3. **Function Timeout**: Vercel has a 10s timeout for Hobby plan - large repos might timeout
4. **Cold Starts**: First request might be slow

## 📝 Example API Response

```json
{
  "repo_name": "facebook/react",
  "repo_url": "https://github.com/facebook/react",
  "languages": {...},
  "structure": {...},
  "patterns": ["React"],
  "recommendations": [...],
  "ai_insights": {
    "architecture_assessment": "...",
    "maturity_level": "...",
    "next_steps": [...]
  }
}
```

## 🎯 Next Steps

1. **Test with your repositories**: Try analyzing your own repos
2. **Customize recommendations**: Edit `github_repo_agent/recommender.py`
3. **Add features**: Extend the agent in `github_repo_agent/agent.py`
4. **Fix Vercel deployment**: Check Vercel logs and settings

---

**Your local setup is working! 🎉**

