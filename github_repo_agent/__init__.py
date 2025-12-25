"""
GitHub Repository Analysis Agent
An intelligent agent that understands your GitHub repositories and provides recommendations.
"""

__version__ = "0.1.0"

from .agent import GitHubRepoAgent, RepoAnalysis
from .github_client import GitHubClient
from .code_analyzer import CodeAnalyzer
from .recommender import Recommender
from .ai_enhancer import AIEnhancer

__all__ = [
    'GitHubRepoAgent',
    'RepoAnalysis',
    'GitHubClient',
    'CodeAnalyzer',
    'Recommender',
    'AIEnhancer',
]

