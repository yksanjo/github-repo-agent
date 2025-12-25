"""
Health check endpoint for Vercel.
"""

import json

# Vercel Python serverless function handler
# This is a function-based handler, NOT a class-based handler
# It does NOT subclass BaseHTTPRequestHandler - it's a simple function
def handler(request):
    """
    Health check handler with error handling.
    
    This is a function-based handler for Vercel Python serverless functions.
    It does NOT subclass BaseHTTPRequestHandler - it's a simple function.
    """
    try:
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Content-Type': 'application/json'
        }
        
        # Get request method
        method = 'GET'
        if isinstance(request, dict):
            method = request.get('method', 'GET')
        elif hasattr(request, 'method'):
            method = request.method
        
        if method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': ''
            }
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'status': 'ok',
                'message': 'GitHub Repository Agent is running on Vercel!',
                'version': '1.0.0'
            })
        }
    except Exception as e:
        # Even health check should handle errors
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'status': 'error',
                'message': f'Health check error: {str(e)}'
            })
        }
