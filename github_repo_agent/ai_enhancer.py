"""
AI-enhanced analysis using built-in capabilities (no external API keys needed).
This module provides enhanced code understanding without requiring OpenAI/Anthropic keys.
"""

import os
import re
from typing import Dict, List, Optional, Any
from pathlib import Path


class AIEnhancer:
    """
    Enhanced AI-powered analysis that works locally without external API keys.
    Uses pattern matching, heuristics, and code analysis for intelligent insights.
    """
    
    def __init__(self):
        """Initialize AI enhancer."""
        self.code_patterns = self._load_code_patterns()
        self.best_practices = self._load_best_practices()
    
    def _load_code_patterns(self) -> Dict[str, List[str]]:
        """Load code patterns for intelligent analysis."""
        return {
            'security_issues': [
                r'password\s*=\s*["\'].*["\']',  # Hardcoded passwords
                r'api[_-]?key\s*=\s*["\'].*["\']',  # Hardcoded API keys
                r'eval\s*\(',  # eval() usage
                r'exec\s*\(',  # exec() usage
                r'sql.*\+.*["\']',  # SQL injection risk
                r'\.innerHTML\s*=',  # XSS risk
            ],
            'performance_issues': [
                r'for\s+.*\s+in\s+range\(len\(',  # Inefficient iteration
                r'\.append\(.*\)\s*$',  # List append in loop
                r'SELECT\s+\*',  # SELECT * queries
            ],
            'code_smells': [
                r'if\s+.*:\s*if\s+.*:\s*if',  # Nested ifs
                r'function\s+\w+\([^)]{100,}\)',  # Long parameter lists
                r'class\s+\w+.*{[\s\S]{1000,}',  # Large classes
            ],
        }
    
    def _load_best_practices(self) -> Dict[str, List[str]]:
        """Load best practice patterns."""
        return {
            'good_practices': [
                'error handling',
                'logging',
                'type hints',
                'docstrings',
                'unit tests',
                'input validation',
            ],
            'architecture_patterns': [
                'dependency injection',
                'repository pattern',
                'service layer',
                'factory pattern',
            ],
        }
    
    def analyze_code_quality(self, repo_path: Optional[Path]) -> Dict[str, Any]:
        """
        Analyze code quality using pattern matching and heuristics.
        
        Args:
            repo_path: Path to repository root
        
        Returns:
            Dictionary with code quality insights
        """
        if not repo_path or not repo_path.exists():
            return {}
        
        insights = {
            'security_concerns': [],
            'performance_opportunities': [],
            'code_smells': [],
            'best_practices_found': [],
            'suggestions': [],
        }
        
        code_extensions = {'.py', '.js', '.ts', '.java', '.go', '.rs', '.rb', '.php', '.cpp', '.c'}
        
        for root, dirs, files in os.walk(repo_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', 'env', 'dist', 'build']]
            
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix.lower() not in code_extensions:
                    continue
                
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    rel_path = file_path.relative_to(repo_path)
                    
                    # Check for security issues
                    for pattern in self.code_patterns['security_issues']:
                        if re.search(pattern, content, re.IGNORECASE):
                            issue_type = self._identify_issue_type(pattern)
                            insights['security_concerns'].append({
                                'file': str(rel_path),
                                'issue': issue_type,
                                'severity': 'high',
                            })
                    
                    # Check for performance issues
                    for pattern in self.code_patterns['performance_issues']:
                        if re.search(pattern, content, re.IGNORECASE):
                            insights['performance_opportunities'].append({
                                'file': str(rel_path),
                                'suggestion': 'Consider optimizing this code pattern',
                            })
                    
                    # Check for code smells
                    for pattern in self.code_patterns['code_smells']:
                        if re.search(pattern, content, re.IGNORECASE):
                            insights['code_smells'].append({
                                'file': str(rel_path),
                                'type': 'complex code structure detected',
                            })
                    
                    # Check for best practices
                    if 'try' in content and 'except' in content:
                        insights['best_practices_found'].append('Error handling')
                    if 'log' in content.lower():
                        insights['best_practices_found'].append('Logging')
                    if file_path.suffix == '.py' and 'def ' in content and '->' in content:
                        insights['best_practices_found'].append('Type hints')
                    if '"""' in content or "'''" in content:
                        insights['best_practices_found'].append('Documentation')
                
                except Exception:
                    continue
        
        # Generate intelligent suggestions
        insights['suggestions'] = self._generate_suggestions(insights)
        
        return insights
    
    def _identify_issue_type(self, pattern: str) -> str:
        """Identify the type of security issue from pattern."""
        if 'password' in pattern:
            return 'Hardcoded password detected'
        elif 'api' in pattern and 'key' in pattern:
            return 'Hardcoded API key detected'
        elif 'eval' in pattern:
            return 'Use of eval() - security risk'
        elif 'sql' in pattern:
            return 'Potential SQL injection risk'
        elif 'innerHTML' in pattern:
            return 'Potential XSS vulnerability'
        return 'Security concern detected'
    
    def _generate_suggestions(self, insights: Dict[str, Any]) -> List[str]:
        """Generate intelligent suggestions based on insights."""
        suggestions = []
        
        if insights['security_concerns']:
            suggestions.append('🔒 Review security concerns - consider using environment variables for secrets')
        
        if len(insights['code_smells']) > 10:
            suggestions.append('🧹 Consider refactoring complex code structures')
        
        if not insights['best_practices_found']:
            suggestions.append('✨ Add error handling, logging, and documentation')
        elif 'Type hints' not in insights['best_practices_found']:
            suggestions.append('💡 Consider adding type hints for better code maintainability')
        
        if insights['performance_opportunities']:
            suggestions.append('⚡ Review performance opportunities for optimization')
        
        return suggestions
    
    def generate_deep_insights(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate deep insights from analysis data.
        
        Args:
            analysis_data: Combined analysis data
        
        Returns:
            Dictionary with deep insights
        """
        insights = {
            'architecture_assessment': self._assess_architecture(analysis_data),
            'maturity_level': self._assess_maturity(analysis_data),
            'next_steps': self._suggest_next_steps(analysis_data),
        }
        
        return insights
    
    def _assess_architecture(self, data: Dict[str, Any]) -> str:
        """Assess architecture quality."""
        patterns = data.get('patterns', [])
        structure = data.get('structure', {})
        metrics = data.get('metrics', {})
        
        score = 0
        if structure.get('has_tests'):
            score += 2
        if structure.get('has_ci'):
            score += 2
        if structure.get('has_docs'):
            score += 1
        if 'Docker' in patterns:
            score += 1
        if 'Testing' in patterns:
            score += 1
        
        if score >= 6:
            return 'Excellent - Well-structured with best practices'
        elif score >= 4:
            return 'Good - Solid foundation with room for improvement'
        elif score >= 2:
            return 'Fair - Basic structure, needs enhancement'
        else:
            return 'Needs Work - Consider adding tests, CI/CD, and documentation'
    
    def _assess_maturity(self, data: Dict[str, Any]) -> str:
        """Assess project maturity level."""
        structure = data.get('structure', {})
        metrics = data.get('metrics', {})
        patterns = data.get('patterns', [])
        
        has_readme = structure.get('has_readme', False)
        has_tests = structure.get('has_tests', False)
        has_ci = structure.get('has_ci', False)
        has_license = structure.get('has_license', False)
        code_files = metrics.get('code_files', 0)
        
        if has_readme and has_tests and has_ci and has_license and code_files > 50:
            return 'Production Ready'
        elif has_readme and (has_tests or has_ci) and code_files > 20:
            return 'Mature'
        elif has_readme and code_files > 10:
            return 'Developing'
        else:
            return 'Early Stage'
    
    def _suggest_next_steps(self, data: Dict[str, Any]) -> List[str]:
        """Suggest next steps for project development."""
        steps = []
        structure = data.get('structure', {})
        patterns = data.get('patterns', [])
        
        if not structure.get('has_tests'):
            steps.append('1. Set up automated testing framework')
        if not structure.get('has_ci'):
            steps.append('2. Implement CI/CD pipeline')
        if 'Docker' not in patterns:
            steps.append('3. Containerize your application')
        if not structure.get('has_docs'):
            steps.append('4. Create comprehensive documentation')
        
        return steps[:5]  # Limit to top 5

