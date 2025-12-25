# 🚀 Deploy to Vercel - Step by Step

## Quick Deploy (5 minutes!)

### Step 1: Prepare Your Code

Your code is already set up for Vercel! The structure is:
```
github-repo-agent/
├── api/              # Serverless functions
├── public/           # Frontend
├── github_repo_agent/ # Main package
└── vercel.json       # Config
```

### Step 2: Push to GitHub

```bash
cd github-repo-agent

# Initialize git if needed
git init

# Add all files
git add .

# Commit
git commit -m "Ready for Vercel deployment"

# Add your GitHub remote (create repo on GitHub first)
git remote add origin https://github.com/YOUR_USERNAME/github-repo-agent.git

# Push
git push -u origin main
```

### Step 3: Deploy to Vercel

**Option A: Via Vercel Dashboard (Recommended)**
1. Go to [vercel.com](https://vercel.com)
2. Sign up/Login (free!)
3. Click "Add New Project"
4. Import your GitHub repository
5. Vercel auto-detects everything
6. Click "Deploy"
7. Wait ~2 minutes
8. **Done!** 🎉

**Option B: Via Vercel CLI**
```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
vercel

# For production
vercel --prod
```

## What Happens

1. Vercel detects Python functions in `/api`
2. Installs dependencies from `requirements.txt`
3. Builds your serverless functions
4. Serves static files from `/public`
5. Your app is live!

## Your Live URL

After deployment, you'll get:
- **Preview URL**: `https://github-repo-agent-xxx.vercel.app`
- **Production URL**: `https://github-repo-agent.vercel.app` (after first deploy)

## Environment Variables (Optional)

If you want GitHub token for private repos:

1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Add: `GITHUB_TOKEN` = `your_token_here`
3. Redeploy

## Features on Vercel

✅ **Works Great:**
- Repository analysis via GitHub API
- Language detection
- Pattern identification
- Recommendations
- AI insights
- Beautiful web interface

⚠️ **Note:**
- Repository cloning is disabled (Vercel file system is read-only)
- Uses GitHub API instead (actually faster!)
- All features still work perfectly

## Custom Domain

1. Vercel Dashboard → Your Project → Settings → Domains
2. Add your domain
3. Follow DNS instructions
4. Done!

## Updates

Just push to GitHub:
```bash
git push origin main
```
Vercel auto-deploys! 🚀

## Troubleshooting

**Build fails?**
- Check `requirements.txt` has all dependencies
- Ensure Python 3.9+ compatibility

**Function timeout?**
- Free tier: 10s timeout
- Hobby: 60s
- Pro: 300s
- Large repos might need Pro tier

**Need help?**
- Check Vercel logs in dashboard
- See `vercel_deploy.md` for detailed guide

---

**Ready to deploy? Just push to GitHub and import to Vercel!** 🎉

