# 🚀 Deploy to Vercel

This guide will help you deploy the GitHub Repository Agent to Vercel.

## Prerequisites

1. A Vercel account (free tier works great!)
2. Vercel CLI installed (optional, but recommended)
3. Git repository (GitHub, GitLab, or Bitbucket)

## Quick Deploy

### Option 1: Deploy via Vercel Dashboard (Easiest)

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Go to Vercel:**
   - Visit [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Vercel will auto-detect the settings
   - Click "Deploy"

3. **That's it!** Your app will be live in minutes.

### Option 2: Deploy via Vercel CLI

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel:**
   ```bash
   vercel login
   ```

3. **Deploy:**
   ```bash
   vercel
   ```

4. **For production:**
   ```bash
   vercel --prod
   ```

## Project Structure for Vercel

```
github-repo-agent/
├── api/                    # Serverless functions
│   ├── __init__.py
│   ├── analyze.py         # Main analysis endpoint
│   └── health.py          # Health check
├── public/                 # Static files
│   └── index.html         # Frontend
├── github_repo_agent/      # Main package
├── vercel.json            # Vercel configuration
└── requirements.txt      # Python dependencies
```

## Configuration

The `vercel.json` file is already configured:
- Python 3.9 runtime
- API routes under `/api/*`
- Static files served from `/public/*`

## Environment Variables (Optional)

If you want to use GitHub token for private repos or higher rate limits:

1. Go to your Vercel project settings
2. Navigate to "Environment Variables"
3. Add: `GITHUB_TOKEN` = `your_token_here`

## Limitations on Vercel

Since Vercel is serverless:
- ❌ Cannot clone repositories (file system is read-only)
- ✅ Uses GitHub API for analysis (faster!)
- ✅ Still provides comprehensive analysis
- ✅ All recommendations work

The agent automatically uses GitHub API when deployed to Vercel, which is actually faster than cloning!

## Custom Domain

1. Go to your project settings in Vercel
2. Navigate to "Domains"
3. Add your custom domain
4. Follow DNS setup instructions

## Monitoring

Vercel provides:
- Real-time logs
- Analytics
- Performance metrics
- Error tracking

Check your Vercel dashboard for all metrics!

## Troubleshooting

### Build Fails
- Check that `requirements.txt` includes all dependencies
- Ensure Python version is compatible (3.9+)

### API Timeout
- Vercel has a 10s timeout for free tier
- Hobby tier: 60s
- Pro tier: 300s
- Large repos might need Pro tier

### CORS Issues
- Already handled in the API functions
- If issues persist, check `vercel.json` routes

## Updates

To update your deployment:
```bash
git push origin main
```
Vercel automatically redeploys on push!

Or manually:
```bash
vercel --prod
```

## Support

- Vercel Docs: https://vercel.com/docs
- Vercel Community: https://github.com/vercel/vercel/discussions

---

**Your app will be live at: `https://your-project.vercel.app`** 🎉

