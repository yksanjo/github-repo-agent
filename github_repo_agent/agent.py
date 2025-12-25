"""
Main agent class for GitHub repository analysis and recommendations.
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime

from .github_client import GitHubClient
from .code_analyzer import CodeAnalyzer
from .recommender import Recommender
from .ai_enhancer import AIEnhancer


@dataclass
class RepoAnalysis:
    """Container for repository analysis results."""
    repo_name: str
    repo_url: str
    languages: Dict[str, float]
    structure: Dict[str, Any]
    dependencies: Dict[str, List[str]]
    patterns: List[str]
    metrics: Dict[str, Any]
    recommendations: List[Dict[str, Any]]
    analyzed_at: str


class GitHubRepoAgent:
    """
    Main agent that analyzes GitHub repositories and provides recommendations.
    """
    
    def __init__(self, github_token: Optional[str] = None, cache_dir: str = ".repo_cache"):
        """
        Initialize the GitHub Repository Agent.
        
        Args:
            github_token: GitHub personal access token (optional, for private repos)
            cache_dir: Directory to cache cloned repositories
        """
        self.github_client = GitHubClient(github_token)
        self.code_analyzer = CodeAnalyzer()
        self.recommender = Recommender()
        self.ai_enhancer = AIEnhancer()
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
    
    def analyze_repo(self, repo_url: str, clone: bool = True) -> RepoAnalysis:
        """
        Analyze a GitHub repository and return comprehensive analysis.
        
        Args:
            repo_url: GitHub repository URL (e.g., 'owner/repo' or full URL)
            clone: Whether to clone the repository locally for analysis
            
        Returns:
            RepoAnalysis object with all analysis results
        """
        # Parse repo URL
        repo_owner, repo_name = self._parse_repo_url(repo_url)
        full_repo_name = f"{repo_owner}/{repo_name}"
        
        print(f"🔍 Analyzing repository: {full_repo_name}")
        
        # Get repository metadata
        repo_info = self.github_client.get_repo_info(repo_owner, repo_name)
        
        # Clone repository if needed
        repo_path = None
        if clone:
            repo_path = self._clone_repo(repo_owner, repo_name)
        
        # Analyze codebase
        print("📊 Analyzing codebase structure...")
        structure = self.code_analyzer.analyze_structure(repo_path) if repo_path else {}
        
        print("🔎 Detecting languages and dependencies...")
        languages = self.code_analyzer.detect_languages(repo_path) if repo_path else {}
        dependencies = self.code_analyzer.extract_dependencies(repo_path) if repo_path else {}
        
        print("🎯 Identifying patterns and best practices...")
        patterns = self.code_analyzer.identify_patterns(repo_path) if repo_path else []
        
        print("📈 Calculating metrics...")
        metrics = self.code_analyzer.calculate_metrics(repo_path) if repo_path else {}
        
        # Generate recommendations
        print("💡 Generating recommendations...")
        recommendations = self.recommender.generate_recommendations(
            repo_info=repo_info,
            structure=structure,
            languages=languages,
            dependencies=dependencies,
            patterns=patterns,
            metrics=metrics
        )
        
        return RepoAnalysis(
            repo_name=full_repo_name,
            repo_url=repo_info.get('html_url', f"https://github.com/{full_repo_name}"),
            languages=languages,
            structure=structure,
            dependencies=dependencies,
            patterns=patterns,
            metrics=metrics,
            recommendations=recommendations,
            analyzed_at=datetime.now().isoformat()
        )
    
    def get_recommendations(self, repo_url: str, focus_area: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get recommendations for a repository, optionally focused on a specific area.
        
        Args:
            repo_url: GitHub repository URL
            focus_area: Optional focus area (e.g., 'security', 'performance', 'architecture')
        
        Returns:
            List of recommendation dictionaries
        """
        analysis = self.analyze_repo(repo_url)
        
        if focus_area:
            return [r for r in analysis.recommendations if focus_area.lower() in r.get('category', '').lower()]
        
        return analysis.recommendations
    
    def suggest_improvements(self, repo_url: str) -> Dict[str, Any]:
        """
        Get a comprehensive improvement plan for a repository.
        
        Args:
            repo_url: GitHub repository URL
        
        Returns:
            Dictionary with improvement suggestions organized by priority
        """
        analysis = self.analyze_repo(repo_url)
        
        improvements = {
            'high_priority': [],
            'medium_priority': [],
            'low_priority': [],
            'quick_wins': []
        }
        
        for rec in analysis.recommendations:
            priority = rec.get('priority', 'medium').lower()
            if priority == 'high':
                improvements['high_priority'].append(rec)
            elif priority == 'low':
                improvements['low_priority'].append(rec)
            else:
                improvements['medium_priority'].append(rec)
            
            if rec.get('effort', 'medium').lower() == 'low':
                improvements['quick_wins'].append(rec)
        
        return improvements
    
    def _parse_repo_url(self, repo_url: str) -> Tuple[str, str]:
        """Parse repository URL into owner and name."""
        # Remove protocol and domain if present
        repo_url = repo_url.replace('https://github.com/', '').replace('http://github.com/', '')
        repo_url = repo_url.replace('git@github.com:', '').replace('.git', '')
        repo_url = repo_url.strip('/')
        
        parts = repo_url.split('/')
        if len(parts) != 2:
            raise ValueError(f"Invalid repository URL format: {repo_url}")
        
        return parts[0], parts[1]
    
    def _clone_repo(self, owner: str, name: str) -> Optional[Path]:
        """Clone repository to cache directory."""
        repo_path = self.cache_dir / name
        
        if repo_path.exists():
            print(f"📦 Using cached repository at {repo_path}")
            return repo_path
        
        repo_url = f"https://github.com/{owner}/{name}.git"
        print(f"📥 Cloning repository to {repo_path}...")
        
        try:
            subprocess.run(
                ['git', 'clone', repo_url, str(repo_path)],
                check=True,
                capture_output=True
            )
            return repo_path
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Failed to clone repository: {e}")
            return None
    
    def export_analysis(self, analysis: RepoAnalysis, output_path: str):
        """Export analysis results to JSON file."""
        with open(output_path, 'w') as f:
            json.dump(asdict(analysis), f, indent=2)
        print(f"✅ Analysis exported to {output_path}")

