"""
Recommendation engine for suggesting improvements and next steps.
"""

from typing import Dict, List, Any, Optional


class Recommender:
    """Generates recommendations based on repository analysis."""
    
    def __init__(self):
        """Initialize recommender."""
        pass
    
    def generate_recommendations(
        self,
        repo_info: Dict[str, Any],
        structure: Dict[str, Any],
        languages: Dict[str, float],
        dependencies: Dict[str, List[str]],
        patterns: List[str],
        metrics: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Generate comprehensive recommendations.
        
        Args:
            repo_info: Repository metadata from GitHub
            structure: Repository structure analysis
            languages: Detected languages
            dependencies: Extracted dependencies
            patterns: Identified patterns
            metrics: Codebase metrics
        
        Returns:
            List of recommendation dictionaries
        """
        recommendations = []
        
        # Structure-based recommendations
        recommendations.extend(self._check_structure(structure))
        
        # Language-specific recommendations
        recommendations.extend(self._check_languages(languages, dependencies))
        
        # Pattern-based recommendations
        recommendations.extend(self._check_patterns(patterns, structure))
        
        # Metrics-based recommendations
        recommendations.extend(self._check_metrics(metrics))
        
        # Security recommendations
        recommendations.extend(self._check_security(dependencies, structure))
        
        # Documentation recommendations
        recommendations.extend(self._check_documentation(structure, repo_info))
        
        # Testing recommendations
        recommendations.extend(self._check_testing(structure, metrics))
        
        # Performance recommendations
        recommendations.extend(self._check_performance(patterns, dependencies))
        
        return recommendations
    
    def _check_structure(self, structure: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check repository structure and recommend improvements."""
        recs = []
        
        if not structure.get('has_readme'):
            recs.append({
                'category': 'Documentation',
                'title': 'Add a README file',
                'description': 'A README helps others understand your project quickly.',
                'priority': 'high',
                'effort': 'low',
                'action': 'Create a README.md file with project description, installation, and usage instructions.'
            })
        
        if not structure.get('has_license'):
            recs.append({
                'category': 'Legal',
                'title': 'Add a LICENSE file',
                'description': 'A license clarifies how others can use your code.',
                'priority': 'medium',
                'effort': 'low',
                'action': 'Choose an appropriate license (MIT, Apache 2.0, GPL, etc.) and add a LICENSE file.'
            })
        
        if not structure.get('has_ci'):
            recs.append({
                'category': 'CI/CD',
                'title': 'Set up Continuous Integration',
                'description': 'CI/CD automates testing and deployment.',
                'priority': 'high',
                'effort': 'medium',
                'action': 'Set up GitHub Actions, GitLab CI, or similar CI/CD pipeline.'
            })
        
        return recs
    
    def _check_languages(self, languages: Dict[str, float], dependencies: Dict[str, List[str]]) -> List[Dict[str, Any]]:
        """Check language usage and recommend best practices."""
        recs = []
        
        if 'python' in languages:
            if 'python' not in dependencies:
                recs.append({
                    'category': 'Dependencies',
                    'title': 'Add dependency management',
                    'description': 'Python projects should use requirements.txt or pyproject.toml.',
                    'priority': 'high',
                    'effort': 'low',
                    'action': 'Create requirements.txt or use Poetry/pipenv for dependency management.'
                })
            
            if languages['python'] > 50:
                recs.append({
                    'category': 'Code Quality',
                    'title': 'Consider adding type hints',
                    'description': 'Type hints improve code maintainability and IDE support.',
                    'priority': 'medium',
                    'effort': 'medium',
                    'action': 'Add type hints to function signatures and use mypy for type checking.'
                })
        
        if 'javascript' in languages or 'typescript' in languages:
            if 'typescript' not in languages and 'javascript' in languages:
                recs.append({
                    'category': 'Code Quality',
                    'title': 'Consider migrating to TypeScript',
                    'description': 'TypeScript provides type safety and better tooling.',
                    'priority': 'low',
                    'effort': 'high',
                    'action': 'Gradually migrate JavaScript files to TypeScript for better type safety.'
                })
            
            if 'javascript' in dependencies or 'typescript' in dependencies:
                deps = dependencies.get('javascript', []) + dependencies.get('typescript', [])
                if len(deps) > 50:
                    recs.append({
                        'category': 'Dependencies',
                        'title': 'Review and optimize dependencies',
                        'description': 'Large dependency trees can increase bundle size and security risks.',
                        'priority': 'medium',
                        'effort': 'medium',
                        'action': 'Audit dependencies, remove unused ones, and consider alternatives.'
                    })
        
        return recs
    
    def _check_patterns(self, patterns: List[str], structure: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check architectural patterns and suggest improvements."""
        recs = []
        
        if 'Docker' not in patterns:
            recs.append({
                'category': 'DevOps',
                'title': 'Consider containerization',
                'description': 'Docker makes deployment and development environments consistent.',
                'priority': 'medium',
                'effort': 'medium',
                'action': 'Create a Dockerfile and optionally docker-compose.yml for easier setup.'
            })
        
        if 'Testing' not in patterns and not structure.get('has_tests'):
            recs.append({
                'category': 'Testing',
                'title': 'Add automated tests',
                'description': 'Tests ensure code quality and prevent regressions.',
                'priority': 'high',
                'effort': 'high',
                'action': 'Set up a testing framework and write unit/integration tests.'
            })
        
        return recs
    
    def _check_metrics(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check codebase metrics and suggest optimizations."""
        recs = []
        
        avg_file_size = metrics.get('avg_file_size', 0)
        if avg_file_size > 500:
            recs.append({
                'category': 'Code Quality',
                'title': 'Consider refactoring large files',
                'description': f'Average file size is {avg_file_size:.0f} lines. Large files are harder to maintain.',
                'priority': 'medium',
                'effort': 'high',
                'action': 'Break down large files into smaller, focused modules.'
            })
        
        test_ratio = 0
        if metrics.get('code_files', 0) > 0:
            test_ratio = metrics.get('test_files', 0) / metrics.get('code_files', 1) * 100
        
        if test_ratio < 20 and metrics.get('code_files', 0) > 10:
            recs.append({
                'category': 'Testing',
                'title': 'Increase test coverage',
                'description': f'Current test coverage appears low ({test_ratio:.1f}%).',
                'priority': 'high',
                'effort': 'high',
                'action': 'Add more unit and integration tests to improve coverage.'
            })
        
        return recs
    
    def _check_security(self, dependencies: Dict[str, List[str]], structure: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check security best practices."""
        recs = []
        
        if dependencies:
            recs.append({
                'category': 'Security',
                'title': 'Regularly update dependencies',
                'description': 'Outdated dependencies may have security vulnerabilities.',
                'priority': 'high',
                'effort': 'low',
                'action': 'Use tools like Dependabot, Snyk, or npm audit to check for vulnerabilities.'
            })
        
        if not structure.get('has_ci'):
            recs.append({
                'category': 'Security',
                'title': 'Add security scanning to CI/CD',
                'description': 'Automated security scanning catches vulnerabilities early.',
                'priority': 'medium',
                'effort': 'low',
                'action': 'Integrate security scanning tools (e.g., CodeQL, Snyk) into your CI pipeline.'
            })
        
        return recs
    
    def _check_documentation(self, structure: Dict[str, Any], repo_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check documentation completeness."""
        recs = []
        
        if not structure.get('has_docs'):
            recs.append({
                'category': 'Documentation',
                'title': 'Add comprehensive documentation',
                'description': 'Good documentation helps users and contributors.',
                'priority': 'medium',
                'effort': 'medium',
                'action': 'Create a docs/ directory with API documentation, guides, and examples.'
            })
        
        if not repo_info.get('description'):
            recs.append({
                'category': 'Documentation',
                'title': 'Add repository description',
                'description': 'A clear description helps others discover and understand your project.',
                'priority': 'low',
                'effort': 'low',
                'action': 'Add a concise description to your GitHub repository.'
            })
        
        return recs
    
    def _check_testing(self, structure: Dict[str, Any], metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check testing setup and coverage."""
        recs = []
        
        if not structure.get('has_tests'):
            recs.append({
                'category': 'Testing',
                'title': 'Set up testing infrastructure',
                'description': 'Automated tests are essential for maintaining code quality.',
                'priority': 'high',
                'effort': 'medium',
                'action': 'Choose a testing framework (Jest, pytest, etc.) and set up test structure.'
            })
        
        return recs
    
    def _check_performance(self, patterns: List[str], dependencies: Dict[str, List[str]]) -> List[Dict[str, Any]]:
        """Check performance optimization opportunities."""
        recs = []
        
        if 'javascript' in dependencies or 'typescript' in dependencies:
            recs.append({
                'category': 'Performance',
                'title': 'Optimize bundle size',
                'description': 'Smaller bundles improve load times and user experience.',
                'priority': 'medium',
                'effort': 'medium',
                'action': 'Use code splitting, tree shaking, and analyze bundle size with webpack-bundle-analyzer.'
            })
        
        return recs

