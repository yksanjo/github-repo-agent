"""
GitHub API client for fetching repository information.
"""

import os
import requests
from typing import Dict, Optional, List
from urllib.parse import urljoin


class GitHubClient:
    """Client for interacting with GitHub API."""
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self, token: Optional[str] = None):
        """
        Initialize GitHub client.
        
        Args:
            token: GitHub personal access token (optional)
        """
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
        }
        if self.token:
            self.headers['Authorization'] = f'token {self.token}'
    
    def get_repo_info(self, owner: str, repo: str) -> Dict:
        """
        Get repository information from GitHub API.
        
        Args:
            owner: Repository owner
            repo: Repository name
        
        Returns:
            Dictionary with repository information
        """
        url = f"{self.BASE_URL}/repos/{owner}/{repo}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Error fetching repo info: {e}")
            return {
                'name': repo,
                'full_name': f"{owner}/{repo}",
                'html_url': f"https://github.com/{owner}/{repo}",
                'description': '',
                'language': None,
                'stargazers_count': 0,
                'forks_count': 0,
                'open_issues_count': 0,
            }
    
    def get_repo_languages(self, owner: str, repo: str) -> Dict[str, int]:
        """
        Get repository language statistics.
        
        Args:
            owner: Repository owner
            repo: Repository name
        
        Returns:
            Dictionary mapping language names to bytes of code
        """
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/languages"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return {}
    
    def get_repo_topics(self, owner: str, repo: str) -> List[str]:
        """
        Get repository topics.
        
        Args:
            owner: Repository owner
            repo: Repository name
        
        Returns:
            List of topic strings
        """
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/topics"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            return data.get('names', [])
        except requests.exceptions.RequestException:
            return []
    
    def get_repo_readme(self, owner: str, repo: str) -> Optional[str]:
        """
        Get repository README content.
        
        Args:
            owner: Repository owner
            repo: Repository name
        
        Returns:
            README content as string, or None if not found
        """
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/readme"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            import base64
            content = response.json().get('content', '')
            return base64.b64decode(content).decode('utf-8')
        except requests.exceptions.RequestException:
            return None

