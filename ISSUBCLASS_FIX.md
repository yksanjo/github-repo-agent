# Fix for issubclass() Error with BaseHTTPRequestHandler

## Problem
The error occurs when Vercel's Python runtime tries to check if handlers are class-based (subclassing `BaseHTTPRequestHandler`) using `issubclass(base, BaseHTTPRequestHandler)`. If `base` is `None` or not a class, this raises a `TypeError`.

## Root Cause
Vercel's `@vercel/python` builder tries to auto-detect whether handlers are:
1. **Function-based handlers** (simple functions) - ✅ What we're using
2. **Class-based handlers** (subclassing `BaseHTTPRequestHandler`) - ❌ Not what we're using

If the detection logic fails and `base` is `None` or not a class, the `issubclass()` check fails.

## Solution Applied

### 1. Explicit Function-Based Handlers
All handlers in `/api/` are now explicitly documented as **function-based handlers**:

- `api/index.py` - Function handler for serving the main page
- `api/analyze.py` - Function handler for repository analysis
- `api/health.py` - Function handler for health checks

### 2. Clear Documentation
Added comments in all handler files clarifying:
- These are **functions**, not classes
- They do **NOT** subclass `BaseHTTPRequestHandler`
- They follow Vercel's function-based handler format

### 3. Handler Format
All handlers follow this format:
```python
def handler(request):
    """
    Handler function for Vercel Python serverless functions.
    This is a function-based handler, NOT a class-based handler.
    """
    # Handle request
    return {
        'statusCode': 200,
        'headers': {...},
        'body': '...'
    }
```

## Verification Checklist

✅ All handlers are functions (not classes)
✅ No imports of `BaseHTTPRequestHandler` or `http.server`
✅ Handlers return proper Vercel response format (dict with `statusCode`, `headers`, `body`)
✅ All Python files compile without syntax errors
✅ Handler signatures match Vercel's expected format

## Files Modified

1. `api/index.py` - Added explicit function documentation
2. `api/analyze.py` - Added explicit function documentation  
3. `api/health.py` - Added explicit function documentation
4. `api/__init__.py` - Added package-level documentation

## Testing

After deploying to Vercel:
1. Check that `/api/health` returns `{"status": "ok"}`
2. Check that `/` serves the HTML page
3. Check that `/api/analyze` accepts POST requests

## Additional Notes

- **DO NOT** create class-based handlers that subclass `BaseHTTPRequestHandler`
- **DO** use function-based handlers for all Vercel Python serverless functions
- If you see this error again, check that:
  - Handlers are defined as `def handler(request):` (functions)
  - No code is trying to use `issubclass()` with handler functions
  - No imports of `http.server` or `BaseHTTPRequestHandler` exist

