# 🚀 Deploy to Vercel in 3 Steps!

## Step 1: Push to GitHub

```bash
cd github-repo-agent
git init
git add .
git commit -m "Ready for Vercel"
git remote add origin https://github.com/YOUR_USERNAME/github-repo-agent.git
git push -u origin main
```

## Step 2: Deploy on Vercel

1. Go to **[vercel.com](https://vercel.com)** and sign up/login (free!)
2. Click **"Add New Project"**
3. **Import** your GitHub repository
4. Vercel auto-detects everything ✅
5. Click **"Deploy"**
6. Wait ~2 minutes ⏳

## Step 3: Done! 🎉

Your app is live at: `https://your-project.vercel.app`

---

## What's Included

✅ **API Functions** (`/api/analyze.py`, `/api/health.py`)
✅ **Frontend** (`/public/index.html`)
✅ **Configuration** (`vercel.json`)
✅ **Dependencies** (`requirements.txt`)

## Optional: Add GitHub Token

For private repos or higher rate limits:

1. Vercel Dashboard → Project → Settings → Environment Variables
2. Add: `GITHUB_TOKEN` = `your_token`
3. Redeploy

## That's It!

No complex setup, no API keys needed (unless you want private repo access). Just push and deploy! 🚀

