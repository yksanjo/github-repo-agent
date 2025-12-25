"""
Code analyzer for understanding repository structure, patterns, and metrics.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from collections import Counter, defaultdict


class CodeAnalyzer:
    """Analyzes codebase structure, patterns, and metrics."""
    
    # Common dependency file patterns
    DEPENDENCY_FILES = {
        'python': ['requirements.txt', 'setup.py', 'pyproject.toml', 'Pipfile', 'poetry.lock'],
        'javascript': ['package.json', 'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml'],
        'typescript': ['package.json', 'package-lock.json', 'yarn.lock', 'tsconfig.json'],
        'java': ['pom.xml', 'build.gradle', 'build.gradle.kts'],
        'go': ['go.mod', 'go.sum'],
        'rust': ['Cargo.toml', 'Cargo.lock'],
        'ruby': ['Gemfile', 'Gemfile.lock'],
        'php': ['composer.json', 'composer.lock'],
    }
    
    # File extensions to language mapping
    LANGUAGE_EXTENSIONS = {
        '.py': 'python',
        '.js': 'javascript',
        '.jsx': 'javascript',
        '.ts': 'typescript',
        '.tsx': 'typescript',
        '.java': 'java',
        '.go': 'go',
        '.rs': 'rust',
        '.rb': 'ruby',
        '.php': 'php',
        '.cpp': 'cpp',
        '.c': 'c',
        '.cs': 'csharp',
        '.swift': 'swift',
        '.kt': 'kotlin',
        '.scala': 'scala',
        '.r': 'r',
        '.m': 'matlab',
        '.sh': 'shell',
        '.bash': 'shell',
        '.zsh': 'shell',
        '.html': 'html',
        '.css': 'css',
        '.scss': 'scss',
        '.sass': 'sass',
        '.vue': 'vue',
        '.dart': 'dart',
    }
    
    def __init__(self):
        """Initialize code analyzer."""
        pass
    
    def analyze_structure(self, repo_path: Optional[Path]) -> Dict[str, Any]:
        """
        Analyze repository structure.
        
        Args:
            repo_path: Path to repository root
        
        Returns:
            Dictionary with structure analysis
        """
        if not repo_path or not repo_path.exists():
            return {}
        
        structure = {
            'has_readme': False,
            'has_license': False,
            'has_ci': False,
            'has_tests': False,
            'has_docs': False,
            'directories': [],
            'config_files': [],
        }
        
        # Common files to check
        common_files = {
            'README': ['readme.md', 'readme.txt', 'readme.rst', 'readme'],
            'LICENSE': ['license', 'license.txt', 'license.md', 'licence'],
            'CI': ['.github/workflows', '.gitlab-ci.yml', '.travis.yml', 'circleci', '.circleci'],
        }
        
        for root, dirs, files in os.walk(repo_path):
            # Skip hidden directories and common ignore patterns
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', 'env']]
            
            rel_root = Path(root).relative_to(repo_path)
            
            # Check for common files
            for file in files:
                file_lower = file.lower()
                if any(pattern in file_lower for pattern in common_files['README']):
                    structure['has_readme'] = True
                if any(pattern in file_lower for pattern in common_files['LICENSE']):
                    structure['has_license'] = True
                if file_lower in ['test', 'tests', 'spec', '__tests__'] or 'test' in str(rel_root).lower():
                    structure['has_tests'] = True
                if 'doc' in str(rel_root).lower() or file_lower.endswith('.md'):
                    structure['has_docs'] = True
            
            # Check for CI/CD
            if any(ci_pattern in str(rel_root) for ci_pattern in common_files['CI']):
                structure['has_ci'] = True
            
            # Collect top-level directories
            if rel_root == Path('.'):
                structure['directories'] = [d for d in dirs if not d.startswith('.')]
        
        return structure
    
    def detect_languages(self, repo_path: Optional[Path]) -> Dict[str, float]:
        """
        Detect programming languages used in repository.
        
        Args:
            repo_path: Path to repository root
        
        Returns:
            Dictionary mapping language names to percentage of code
        """
        if not repo_path or not repo_path.exists():
            return {}
        
        language_files = Counter()
        total_files = 0
        
        for root, dirs, files in os.walk(repo_path):
            # Skip common ignore patterns
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', 'env', 'dist', 'build']]
            
            for file in files:
                if file.startswith('.'):
                    continue
                
                ext = Path(file).suffix.lower()
                if ext in self.LANGUAGE_EXTENSIONS:
                    language = self.LANGUAGE_EXTENSIONS[ext]
                    language_files[language] += 1
                    total_files += 1
        
        if total_files == 0:
            return {}
        
        # Convert to percentages
        return {lang: (count / total_files) * 100 for lang, count in language_files.items()}
    
    def extract_dependencies(self, repo_path: Optional[Path]) -> Dict[str, List[str]]:
        """
        Extract dependencies from dependency files.
        
        Args:
            repo_path: Path to repository root
        
        Returns:
            Dictionary mapping language to list of dependencies
        """
        if not repo_path or not repo_path.exists():
            return {}
        
        dependencies = {}
        
        for language, files in self.DEPENDENCY_FILES.items():
            deps = []
            for dep_file in files:
                file_path = repo_path / dep_file
                if file_path.exists():
                    deps.extend(self._parse_dependency_file(file_path, language))
            
            if deps:
                dependencies[language] = list(set(deps))  # Remove duplicates
        
        return dependencies
    
    def _parse_dependency_file(self, file_path: Path, language: str) -> List[str]:
        """Parse a dependency file and extract package names."""
        deps = []
        
        try:
            content = file_path.read_text()
            
            if language == 'python':
                if file_path.name == 'requirements.txt':
                    # Parse requirements.txt
                    for line in content.split('\n'):
                        line = line.strip()
                        if line and not line.startswith('#'):
                            # Extract package name (before ==, >=, etc.)
                            dep = re.split(r'[>=<!=]', line)[0].strip()
                            if dep:
                                deps.append(dep)
                elif file_path.name in ['setup.py', 'pyproject.toml']:
                    # Basic extraction - could be improved
                    matches = re.findall(r'["\']([^"\']+)["\']', content)
                    deps.extend(matches[:20])  # Limit to avoid noise
            
            elif language in ['javascript', 'typescript']:
                if file_path.name == 'package.json':
                    import json
                    try:
                        data = json.loads(content)
                        deps.extend(data.get('dependencies', {}).keys())
                        deps.extend(data.get('devDependencies', {}).keys())
                    except:
                        pass
            
            elif language == 'java':
                if 'pom.xml' in str(file_path):
                    # Basic XML parsing for dependencies
                    matches = re.findall(r'<artifactId>([^<]+)</artifactId>', content)
                    deps.extend(matches)
            
            elif language == 'go':
                if file_path.name == 'go.mod':
                    for line in content.split('\n'):
                        if line.strip().startswith('require'):
                            parts = line.split()
                            if len(parts) > 1:
                                deps.append(parts[1])
        
        except Exception as e:
            pass  # Silently fail for unparseable files
        
        return deps
    
    def identify_patterns(self, repo_path: Optional[Path]) -> List[str]:
        """
        Identify architectural patterns and practices.
        
        Args:
            repo_path: Path to repository root
        
        Returns:
            List of identified patterns
        """
        if not repo_path or not repo_path.exists():
            return []
        
        patterns = []
        
        # Check for common patterns
        patterns_to_check = {
            'MVC': ['models', 'views', 'controllers'],
            'REST API': ['api', 'routes', 'endpoints'],
            'Microservices': ['services', 'microservice'],
            'Docker': ['Dockerfile', 'docker-compose'],
            'Kubernetes': ['k8s', 'kubernetes', 'deployment.yaml'],
            'Testing': ['test', 'spec', '__tests__', 'tests'],
            'CI/CD': ['.github/workflows', '.gitlab-ci.yml', '.travis.yml'],
            'TypeScript': ['tsconfig.json', '.ts'],
            'React': ['react', 'jsx', 'tsx'],
            'Vue': ['vue.config.js', '.vue'],
            'Django': ['manage.py', 'settings.py'],
            'Flask': ['app.py', 'flask'],
            'Express': ['express', 'app.js', 'server.js'],
        }
        
        repo_str = str(repo_path).lower()
        file_list = []
        for root, dirs, files in os.walk(repo_path):
            file_list.extend([f.lower() for f in files])
            file_list.extend([d.lower() for d in dirs])
        
        all_content = ' '.join(file_list) + ' ' + repo_str
        
        for pattern_name, indicators in patterns_to_check.items():
            if any(ind.lower() in all_content for ind in indicators):
                patterns.append(pattern_name)
        
        return list(set(patterns))
    
    def calculate_metrics(self, repo_path: Optional[Path]) -> Dict[str, Any]:
        """
        Calculate codebase metrics.
        
        Args:
            repo_path: Path to repository root
        
        Returns:
            Dictionary with various metrics
        """
        if not repo_path or not repo_path.exists():
            return {}
        
        metrics = {
            'total_files': 0,
            'total_lines': 0,
            'code_files': 0,
            'test_files': 0,
            'avg_file_size': 0,
        }
        
        code_extensions = set(self.LANGUAGE_EXTENSIONS.keys())
        total_lines = 0
        code_file_count = 0
        
        for root, dirs, files in os.walk(repo_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', 'env', 'dist', 'build']]
            
            for file in files:
                if file.startswith('.'):
                    continue
                
                file_path = Path(root) / file
                ext = file_path.suffix.lower()
                
                metrics['total_files'] += 1
                
                if ext in code_extensions:
                    code_file_count += 1
                    if 'test' in str(file_path).lower():
                        metrics['test_files'] += 1
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = len(f.readlines())
                            total_lines += lines
                    except:
                        pass
        
        metrics['code_files'] = code_file_count
        metrics['total_lines'] = total_lines
        if code_file_count > 0:
            metrics['avg_file_size'] = total_lines / code_file_count
        
        return metrics

