#!/usr/bin/env python3
"""
Example usage of the GitHub Repository Agent.
"""

from github_repo_agent import GitHubRepoAgent

def main():
    # Initialize the agent
    # You can optionally provide a GitHub token for private repos or higher rate limits
    agent = GitHubRepoAgent(github_token=None)  # or os.getenv('GITHUB_TOKEN')
    
    # Example: Analyze a public repository
    repo_url = "facebook/react"  # or "https://github.com/facebook/react"
    
    print("="*70)
    print("GitHub Repository Agent - Example Usage")
    print("="*70)
    
    # Get comprehensive analysis
    print(f"\n1. Analyzing repository: {repo_url}")
    analysis = agent.analyze_repo(repo_url, clone=True)
    
    print(f"\n✅ Analysis complete!")
    print(f"   Repository: {analysis.repo_name}")
    print(f"   Languages: {', '.join(analysis.languages.keys())}")
    print(f"   Patterns: {', '.join(analysis.patterns)}")
    print(f"   Total recommendations: {len(analysis.recommendations)}")
    
    # Get focused recommendations
    print(f"\n2. Getting security recommendations...")
    security_recs = agent.get_recommendations(repo_url, focus_area="security")
    print(f"   Found {len(security_recs)} security recommendations")
    
    # Get improvement plan
    print(f"\n3. Getting improvement plan...")
    improvements = agent.suggest_improvements(repo_url)
    print(f"   Quick wins: {len(improvements['quick_wins'])}")
    print(f"   High priority: {len(improvements['high_priority'])}")
    print(f"   Medium priority: {len(improvements['medium_priority'])}")
    print(f"   Low priority: {len(improvements['low_priority'])}")
    
    # Export analysis
    print(f"\n4. Exporting analysis...")
    agent.export_analysis(analysis, "example_analysis.json")
    
    print("\n" + "="*70)
    print("Example complete! Check example_analysis.json for full results.")
    print("="*70)

if __name__ == '__main__':
    main()

