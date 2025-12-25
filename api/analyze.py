"""
Vercel serverless function for repository analysis.
"""

import json
import os
import traceback
import re

# Vercel Python serverless function handler
# This is a function-based handler, NOT a class-based handler
# It does NOT subclass BaseHTTPRequestHandler - it's a simple function
def handler(request):
    """
    Vercel serverless function handler with comprehensive error handling.
    
    This is a function-based handler for Vercel Python serverless functions.
    It does NOT subclass BaseHTTPRequestHandler - it's a simple function.
    """
    try:
        # Log request for debugging
        print(f"Analyze handler called with request type: {type(request)}")
        
        # Import here to avoid cold start issues
        from github_repo_agent import GitHubRepoAgent
        from github_repo_agent.ai_enhancer import AIEnhancer
        
        # Initialize agents
        github_token = os.getenv('GITHUB_TOKEN')
        agent = GitHubRepoAgent(github_token=github_token)
        ai_enhancer = AIEnhancer()
        
        # Handle CORS
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS, GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Content-Type': 'application/json'
        }
        
        # Get request method - handle both dict and object formats
        method = 'GET'
        if isinstance(request, dict):
            method = request.get('method', 'GET')
        elif hasattr(request, 'method'):
            method = request.method
        
        # Handle preflight
        if method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': ''
            }
        
        # Get request body
        if method == 'POST':
            # Parse request body
            body = {}
            try:
                if isinstance(request, dict):
                    body_data = request.get('body', {})
                    if isinstance(body_data, str):
                        body = json.loads(body_data)
                    elif isinstance(body_data, dict):
                        body = body_data
                elif hasattr(request, 'json') and request.json:
                    body = request.json
                elif hasattr(request, 'body') and request.body:
                    if isinstance(request.body, str):
                        body = json.loads(request.body)
                    elif isinstance(request.body, dict):
                        body = request.body
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                body = {}
            except Exception as e:
                print(f"Error parsing body: {e}")
                body = {}
            
            repo_url = body.get('repo_url') if body else None
            
            # Also check query params
            if not repo_url:
                if isinstance(request, dict):
                    query = request.get('query', {})
                    repo_url = query.get('repo_url') if query else None
                elif hasattr(request, 'args') and request.args:
                    repo_url = request.args.get('repo_url')
            
            if not repo_url:
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({
                        'error': 'Repository URL is required',
                        'hint': 'Please provide a repository in format: owner/repo or https://github.com/owner/repo'
                    })
                }
            
            # Normalize repository URL
            repo_url = normalize_repo_url(repo_url)
            if not repo_url:
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({
                        'error': 'Invalid repository format',
                        'hint': 'Please use format: owner/repo (e.g., facebook/react) or https://github.com/owner/repo'
                    })
                }
            
            print(f"Analyzing repository: {repo_url}")
            
            # Perform analysis (without cloning for Vercel - use GitHub API only)
            try:
                analysis = agent.analyze_repo(repo_url, clone=False)
            except ValueError as e:
                # Handle invalid repository format
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({
                        'error': str(e),
                        'hint': 'Please check that the repository exists and is accessible'
                    })
                }
            except Exception as e:
                # Handle other analysis errors
                error_msg = str(e)
                print(f"Analysis error: {error_msg}")
                print(traceback.format_exc())
                
                # Check if it's a GitHub API error
                if '404' in error_msg or 'Not Found' in error_msg:
                    return {
                        'statusCode': 404,
                        'headers': headers,
                        'body': json.dumps({
                            'error': 'Repository not found',
                            'hint': 'The repository may not exist, be private, or you may not have access. Please verify the repository URL.'
                        })
                    }
                elif '403' in error_msg or 'Forbidden' in error_msg:
                    return {
                        'statusCode': 403,
                        'headers': headers,
                        'body': json.dumps({
                            'error': 'Access forbidden',
                            'hint': 'This repository may be private. If you own it, add a GITHUB_TOKEN environment variable in Vercel settings.'
                        })
                    }
                else:
                    return {
                        'statusCode': 500,
                        'headers': headers,
                        'body': json.dumps({
                            'error': f'Analysis failed: {error_msg}',
                            'hint': 'Please try again or check if the repository is accessible'
                        })
                    }
            
            # Get AI-enhanced insights
            analysis_dict = {
                'repo_name': analysis.repo_name,
                'repo_url': analysis.repo_url,
                'languages': analysis.languages,
                'structure': analysis.structure,
                'dependencies': analysis.dependencies,
                'patterns': analysis.patterns,
                'metrics': analysis.metrics,
                'recommendations': analysis.recommendations,
            }
            
            # Add AI insights
            try:
                ai_insights = ai_enhancer.generate_deep_insights(analysis_dict)
                analysis_dict['ai_insights'] = ai_insights
            except Exception as e:
                print(f"Error generating AI insights: {e}")
                analysis_dict['ai_insights'] = {}
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(analysis_dict)
            }
        
        # GET request - return info
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'message': 'GitHub Repository Agent API',
                'endpoint': '/api/analyze',
                'method': 'POST',
                'body': {'repo_url': 'owner/repo'},
                'examples': [
                    'facebook/react',
                    'microsoft/vscode',
                    'https://github.com/torvalds/linux'
                ]
            })
        }
    
    except ImportError as e:
        # Handle import errors gracefully
        error_msg = f"Import error: {str(e)}"
        print(error_msg)
        print(traceback.format_exc())
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': 'Internal server error - dependencies not available',
                'type': 'ImportError',
                'hint': 'Please contact support if this persists'
            })
        }
    except Exception as e:
        # Comprehensive error handling
        error_msg = str(e)
        error_type = type(e).__name__
        traceback_str = traceback.format_exc()
        
        # Log error for debugging
        print(f"Error in analyze handler: {error_msg}")
        print(f"Error type: {error_type}")
        print(traceback_str)
        
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': error_msg,
                'type': error_type,
                'hint': 'Please try again or check the repository URL format'
            })
        }


def normalize_repo_url(repo_url):
    """
    Normalize repository URL to owner/repo format.
    
    Examples:
    - 'facebook/react' -> 'facebook/react'
    - 'https://github.com/facebook/react' -> 'facebook/react'
    - 'https://github.com/facebook/react.git' -> 'facebook/react'
    - 'github.com/facebook/react' -> 'facebook/react'
    """
    if not repo_url:
        return None
    
    repo_url = str(repo_url).strip()
    
    # Remove protocol and domain
    repo_url = re.sub(r'^https?://(www\.)?github\.com/', '', repo_url, flags=re.IGNORECASE)
    repo_url = re.sub(r'^github\.com/', '', repo_url, flags=re.IGNORECASE)
    repo_url = re.sub(r'^git@github\.com:', '', repo_url, flags=re.IGNORECASE)
    
    # Remove .git extension (must be at end)
    if repo_url.endswith('.git'):
        repo_url = repo_url[:-4]
    
    # Remove trailing slashes
    repo_url = repo_url.rstrip('/')
    
    # Remove leading slashes
    repo_url = repo_url.lstrip('/')
    
    # Validate format: should be owner/repo
    parts = repo_url.split('/')
    if len(parts) != 2:
        return None
    
    owner = parts[0].strip()
    repo = parts[1].strip()
    
    # Remove any query params or fragments from repo name
    repo = repo.split('?')[0].split('#')[0].strip()
    
    if not owner or not repo:
        return None
    
    return f"{owner}/{repo}"
