# 🔧 Troubleshooting 404 Errors on Vercel

## Common Issues and Solutions

### 1. 404 on API Endpoints

**Problem:** `/api/analyze` returns 404

**Solutions:**

#### Check Vercel Configuration
- Ensure `vercel.json` has correct routes
- Verify Python functions are in `/api/` directory
- Check that `requirements.txt` includes all dependencies

#### Verify Function Format
Vercel Python functions need:
```python
def handler(request):
    return {
        'statusCode': 200,
        'headers': {...},
        'body': json.dumps({...})
    }
```

#### Check Build Logs
1. Go to Vercel Dashboard
2. Click on your project
3. Check "Deployments" tab
4. Click on latest deployment
5. Check "Build Logs" for errors

### 2. Frontend Can't Find API

**Problem:** Frontend loads but API calls fail

**Solution:** Update API URL in `public/index.html`:
```javascript
const API_URL = window.location.origin + '/api';
```

### 3. CORS Errors

**Problem:** CORS errors in browser console

**Solution:** Already handled in API functions, but verify headers:
```python
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS, GET',
    'Access-Control-Allow-Headers': 'Content-Type',
}
```

### 4. Function Timeout

**Problem:** Request times out

**Solution:**
- Free tier: 10s timeout
- Hobby: 60s timeout  
- Pro: 300s timeout
- Large repos might need Pro tier

### 5. Import Errors

**Problem:** Module not found errors

**Solution:**
- Check `requirements.txt` has all dependencies
- Ensure `github_repo_agent` package is included
- Verify Python version (3.9+)

## Debugging Steps

### Step 1: Check Function Logs
1. Vercel Dashboard → Project → Functions
2. Click on function (e.g., `/api/analyze`)
3. Check "Logs" tab

### Step 2: Test Health Endpoint
```bash
curl https://your-project.vercel.app/api/health
```

Should return:
```json
{"status": "ok", "message": "GitHub Repository Agent is running on Vercel!"}
```

### Step 3: Test Analyze Endpoint
```bash
curl -X POST https://your-project.vercel.app/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "facebook/react"}'
```

### Step 4: Check Browser Console
- Open browser DevTools (F12)
- Check Console tab for errors
- Check Network tab for failed requests

## Quick Fixes

### Fix 1: Update vercel.json
```json
{
  "routes": [
    {
      "src": "/api/analyze",
      "dest": "/api/analyze.py"
    },
    {
      "src": "/(.*)",
      "dest": "/public/$1"
    }
  ]
}
```

### Fix 2: Verify File Structure
```
github-repo-agent/
├── api/
│   ├── analyze.py
│   ├── health.py
│   └── index.py
├── public/
│   └── index.html
└── vercel.json
```

### Fix 3: Redeploy
```bash
# Push changes
git add .
git commit -m "Fix routing"
git push

# Vercel auto-deploys, or manually:
vercel --prod
```

## Still Having Issues?

1. **Check Vercel Status:** https://vercel-status.com
2. **Review Documentation:** https://vercel.com/docs
3. **Check Community:** https://github.com/vercel/vercel/discussions

## Common Error Messages

### "Module not found"
→ Add missing package to `requirements.txt`

### "Function timeout"
→ Upgrade to Pro tier or optimize code

### "404 Not Found"
→ Check `vercel.json` routes configuration

### "Internal Server Error"
→ Check function logs in Vercel dashboard

---

**Need more help?** Check the build logs in Vercel dashboard for detailed error messages!

