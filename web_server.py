#!/usr/bin/env python3
"""
Local web server for GitHub Repository Agent.
Launch this to use the agent through a web interface - no API keys needed!
"""

from flask import Flask, render_template_string, request, jsonify
from github_repo_agent import GitHubRepoAgent
from github_repo_agent.ai_enhancer import AIEnhancer
import json

app = Flask(__name__)
agent = GitHubRepoAgent()
ai_enhancer = AIEnhancer()

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub Repository Agent</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header p { opacity: 0.9; font-size: 1.1em; }
        .content {
            padding: 40px;
        }
        .input-section {
            background: #f8f9fa;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
        }
        input[type="text"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 14px 30px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
            color: #667eea;
        }
        .results {
            display: none;
            margin-top: 30px;
        }
        .result-section {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .result-section h3 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        .badge {
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            margin: 5px;
        }
        .badge-success { background: #d4edda; color: #155724; }
        .badge-warning { background: #fff3cd; color: #856404; }
        .badge-danger { background: #f8d7da; color: #721c24; }
        .badge-info { background: #d1ecf1; color: #0c5460; }
        .recommendation {
            background: white;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 10px;
            border-left: 4px solid #667eea;
        }
        .recommendation h4 {
            color: #333;
            margin-bottom: 8px;
        }
        .recommendation p {
            color: #666;
            line-height: 1.6;
        }
        .priority-high { border-left-color: #dc3545; }
        .priority-medium { border-left-color: #ffc107; }
        .priority-low { border-left-color: #28a745; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 GitHub Repository Agent</h1>
            <p>Analyze any GitHub repository and get intelligent recommendations - No API keys needed!</p>
        </div>
        <div class="content">
            <div class="input-section">
                <form id="analyzeForm" onsubmit="analyzeRepo(event)">
                    <div class="form-group">
                        <label for="repoUrl">Repository URL or owner/repo:</label>
                        <input type="text" id="repoUrl" name="repoUrl" 
                               placeholder="e.g., facebook/react or https://github.com/facebook/react" 
                               required>
                    </div>
                    <button type="submit">🔍 Analyze Repository</button>
                </form>
            </div>
            
            <div class="loading" id="loading">
                <p>⏳ Analyzing repository... This may take a moment.</p>
            </div>
            
            <div class="results" id="results"></div>
        </div>
    </div>

    <script>
        async function analyzeRepo(event) {
            event.preventDefault();
            const repoUrl = document.getElementById('repoUrl').value;
            const loading = document.getElementById('loading');
            const results = document.getElementById('results');
            
            loading.style.display = 'block';
            results.style.display = 'none';
            results.innerHTML = '';
            
            try {
                const response = await fetch('/api/analyze', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({repo_url: repoUrl})
                });
                
                const data = await response.json();
                displayResults(data);
            } catch (error) {
                results.innerHTML = '<div class="result-section"><h3>❌ Error</h3><p>' + error.message + '</p></div>';
                results.style.display = 'block';
            } finally {
                loading.style.display = 'none';
            }
        }
        
        function displayResults(data) {
            const results = document.getElementById('results');
            let html = '';
            
            // Overview
            html += '<div class="result-section"><h3>📊 Overview</h3>';
            html += '<p><strong>Repository:</strong> ' + data.repo_name + '</p>';
            html += '<p><strong>URL:</strong> <a href="' + data.repo_url + '" target="_blank">' + data.repo_url + '</a></p>';
            html += '</div>';
            
            // Languages
            if (data.languages && Object.keys(data.languages).length > 0) {
                html += '<div class="result-section"><h3>📝 Languages</h3>';
                for (const [lang, pct] of Object.entries(data.languages)) {
                    html += '<span class="badge badge-info">' + lang + ': ' + pct.toFixed(1) + '%</span>';
                }
                html += '</div>';
            }
            
            // Structure
            if (data.structure) {
                html += '<div class="result-section"><h3>🏗️ Structure</h3>';
                const s = data.structure;
                html += '<span class="badge ' + (s.has_readme ? 'badge-success' : 'badge-warning') + '">README</span>';
                html += '<span class="badge ' + (s.has_license ? 'badge-success' : 'badge-warning') + '">LICENSE</span>';
                html += '<span class="badge ' + (s.has_ci ? 'badge-success' : 'badge-warning') + '">CI/CD</span>';
                html += '<span class="badge ' + (s.has_tests ? 'badge-success' : 'badge-warning') + '">Tests</span>';
                html += '</div>';
            }
            
            // Patterns
            if (data.patterns && data.patterns.length > 0) {
                html += '<div class="result-section"><h3>🎯 Patterns</h3>';
                data.patterns.forEach(p => {
                    html += '<span class="badge badge-info">' + p + '</span>';
                });
                html += '</div>';
            }
            
            // Recommendations
            if (data.recommendations && data.recommendations.length > 0) {
                html += '<div class="result-section"><h3>💡 Recommendations</h3>';
                data.recommendations.forEach(rec => {
                    const priority = rec.priority || 'medium';
                    html += '<div class="recommendation priority-' + priority + '">';
                    html += '<h4>' + rec.title + '</h4>';
                    html += '<p><strong>Category:</strong> ' + rec.category + '</p>';
                    html += '<p>' + rec.description + '</p>';
                    html += '<p><strong>Action:</strong> ' + rec.action + '</p>';
                    html += '</div>';
                });
                html += '</div>';
            }
            
            // AI Insights
            if (data.ai_insights) {
                html += '<div class="result-section"><h3>🤖 AI Insights</h3>';
                if (data.ai_insights.architecture_assessment) {
                    html += '<p><strong>Architecture:</strong> ' + data.ai_insights.architecture_assessment + '</p>';
                }
                if (data.ai_insights.maturity_level) {
                    html += '<p><strong>Maturity Level:</strong> ' + data.ai_insights.maturity_level + '</p>';
                }
                if (data.ai_insights.next_steps && data.ai_insights.next_steps.length > 0) {
                    html += '<p><strong>Next Steps:</strong></p><ul>';
                    data.ai_insights.next_steps.forEach(step => {
                        html += '<li>' + step + '</li>';
                    });
                    html += '</ul>';
                }
                html += '</div>';
            }
            
            results.innerHTML = html;
            results.style.display = 'block';
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main page."""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """API endpoint for repository analysis."""
    try:
        data = request.json
        repo_url = data.get('repo_url')
        
        if not repo_url:
            return jsonify({'error': 'Repository URL is required'}), 400
        
        # Perform analysis
        analysis = agent.analyze_repo(repo_url, clone=True)
        
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
        ai_insights = ai_enhancer.generate_deep_insights(analysis_dict)
        analysis_dict['ai_insights'] = ai_insights
        
        # Add code quality analysis if repo was cloned
        repo_path = agent.cache_dir / repo_url.split('/')[-1]
        if repo_path.exists():
            code_quality = ai_enhancer.analyze_code_quality(repo_path)
            analysis_dict['code_quality'] = code_quality
        
        return jsonify(analysis_dict)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok', 'message': 'GitHub Repository Agent is running'})

if __name__ == '__main__':
    import socket
    import sys
    
    # Find an available port (start from 5001 since 5000 is often used by AirPlay on macOS)
    def find_free_port(start_port=5001):
        for port in range(start_port, start_port + 50):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('', port))
                    return port
            except OSError:
                continue
        return 8080  # Fallback
    
    port = find_free_port()
    
    print("="*70)
    print("🚀 GitHub Repository Agent - Local Web Server")
    print("="*70)
    print(f"\n📍 Server starting at: http://localhost:{port}")
    print("💡 Open your browser and navigate to the URL above")
    print("🔒 No API keys needed - everything runs locally!")
    print(f"\n💻 To stop the server, press Ctrl+C")
    print("\n" + "="*70 + "\n")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=port, use_reloader=False)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")
        sys.exit(0)

