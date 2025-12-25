# ⚙️ Vercel Settings Configuration Guide

## Current Issue
API endpoints returning 404 - Python functions not being detected.

## Fix in Vercel Dashboard

### Step 1: Go to Project Settings
1. Visit: https://vercel.com/yoshi-kondos-projects/github-repo-agent/settings
2. Click on **"Build & Development Settings"**

### Step 2: Configure Settings
Set these values:

- **Framework Preset**: `Other` or `Python`
- **Root Directory**: `.` (dot) or leave empty
- **Build Command**: (leave empty)
- **Output Directory**: (leave empty)  
- **Install Command**: `pip install -r requirements.txt`
- **Node.js Version**: (not needed, but if present, set to latest)

### Step 3: Environment Variables (Optional)
If you want to use GitHub token for private repos:
- Go to **"Environment Variables"**
- Add: `GITHUB_TOKEN` = `your_token_here`
- Select environments: Production, Preview, Development

### Step 4: Save and Redeploy
1. Click **"Save"**
2. Go to **"Deployments"** tab
3. Click **"Redeploy"** on latest deployment
4. Or trigger new deployment from Git

## Alternative: Check Function Detection

1. Go to latest deployment
2. Click **"Functions"** tab
3. You should see:
   - `/api/analyze.py`
   - `/api/health.py`
   - `/api/index.py`

If they're missing, Vercel isn't detecting Python functions.

## Verification

After configuration, test:
- ✅ `https://your-app.vercel.app/api/health` → Should return JSON
- ✅ `https://your-app.vercel.app/api/analyze` → Should accept POST
- ✅ `https://your-app.vercel.app/` → Should show UI

## Current Production Domain

**https://github-repo-agent-yoshi-kondos-projects.vercel.app**

Try this domain - it might already be configured correctly!




