#!/usr/bin/env python3
"""
Command-line interface for GitHub Repository Agent.
"""

import argparse
import json
import sys
from pathlib import Path

from github_repo_agent.agent import GitHubRepoAgent


def print_analysis(analysis):
    """Pretty print analysis results."""
    print("\n" + "="*70)
    print(f"📊 Repository Analysis: {analysis.repo_name}")
    print("="*70)
    
    print(f"\n🔗 URL: {analysis.repo_url}")
    print(f"⏰ Analyzed at: {analysis.analyzed_at}")
    
    # Languages
    if analysis.languages:
        print("\n📝 Languages Detected:")
        for lang, percentage in sorted(analysis.languages.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {lang}: {percentage:.1f}%")
    
    # Structure
    if analysis.structure:
        print("\n🏗️  Repository Structure:")
        structure = analysis.structure
        print(f"   • Has README: {'✅' if structure.get('has_readme') else '❌'}")
        print(f"   • Has LICENSE: {'✅' if structure.get('has_license') else '❌'}")
        print(f"   • Has CI/CD: {'✅' if structure.get('has_ci') else '❌'}")
        print(f"   • Has Tests: {'✅' if structure.get('has_tests') else '❌'}")
        print(f"   • Has Docs: {'✅' if structure.get('has_docs') else '❌'}")
    
    # Patterns
    if analysis.patterns:
        print("\n🎯 Patterns Identified:")
        for pattern in analysis.patterns:
            print(f"   • {pattern}")
    
    # Metrics
    if analysis.metrics:
        print("\n📈 Codebase Metrics:")
        metrics = analysis.metrics
        print(f"   • Total Files: {metrics.get('total_files', 0)}")
        print(f"   • Code Files: {metrics.get('code_files', 0)}")
        print(f"   • Test Files: {metrics.get('test_files', 0)}")
        print(f"   • Total Lines: {metrics.get('total_lines', 0):,}")
        print(f"   • Avg File Size: {metrics.get('avg_file_size', 0):.1f} lines")
    
    # Recommendations
    if analysis.recommendations:
        print("\n💡 Recommendations:")
        print("-" * 70)
        
        # Group by priority
        high_priority = [r for r in analysis.recommendations if r.get('priority') == 'high']
        medium_priority = [r for r in analysis.recommendations if r.get('priority') == 'medium']
        low_priority = [r for r in analysis.recommendations if r.get('priority') == 'low']
        
        if high_priority:
            print("\n🔴 High Priority:")
            for i, rec in enumerate(high_priority, 1):
                print(f"\n   {i}. {rec.get('title')}")
                print(f"      Category: {rec.get('category')}")
                print(f"      {rec.get('description')}")
                print(f"      Action: {rec.get('action')}")
                print(f"      Effort: {rec.get('effort', 'medium').title()}")
        
        if medium_priority:
            print("\n🟡 Medium Priority:")
            for i, rec in enumerate(medium_priority, 1):
                print(f"\n   {i}. {rec.get('title')}")
                print(f"      Category: {rec.get('category')}")
                print(f"      {rec.get('description')}")
                print(f"      Action: {rec.get('action')}")
        
        if low_priority:
            print("\n🟢 Low Priority:")
            for i, rec in enumerate(low_priority, 1):
                print(f"\n   {i}. {rec.get('title')}")
                print(f"      Category: {rec.get('category')}")
                print(f"      {rec.get('description')}")
    
    print("\n" + "="*70)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='GitHub Repository Analysis Agent - Understand and improve your repositories',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a repository
  python cli.py analyze owner/repo
  
  # Get recommendations only
  python cli.py recommend owner/repo
  
  # Get security-focused recommendations
  python cli.py recommend owner/repo --focus security
  
  # Export analysis to JSON
  python cli.py analyze owner/repo --export analysis.json
  
  # Get improvement plan
  python cli.py improve owner/repo
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze a repository')
    analyze_parser.add_argument('repo', help='Repository URL or owner/repo format')
    analyze_parser.add_argument('--no-clone', action='store_true', help='Skip cloning repository')
    analyze_parser.add_argument('--export', help='Export analysis to JSON file')
    analyze_parser.add_argument('--token', help='GitHub personal access token')
    
    # Recommend command
    recommend_parser = subparsers.add_parser('recommend', help='Get recommendations for a repository')
    recommend_parser.add_argument('repo', help='Repository URL or owner/repo format')
    recommend_parser.add_argument('--focus', help='Focus area (e.g., security, performance, testing)')
    recommend_parser.add_argument('--token', help='GitHub personal access token')
    
    # Improve command
    improve_parser = subparsers.add_parser('improve', help='Get improvement plan for a repository')
    improve_parser.add_argument('repo', help='Repository URL or owner/repo format')
    improve_parser.add_argument('--token', help='GitHub personal access token')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Initialize agent
    agent = GitHubRepoAgent(github_token=args.token if hasattr(args, 'token') and args.token else None)
    
    try:
        if args.command == 'analyze':
            analysis = agent.analyze_repo(args.repo, clone=not args.no_clone)
            print_analysis(analysis)
            
            if hasattr(args, 'export') and args.export:
                agent.export_analysis(analysis, args.export)
        
        elif args.command == 'recommend':
            focus = args.focus if hasattr(args, 'focus') else None
            recommendations = agent.get_recommendations(args.repo, focus_area=focus)
            
            print(f"\n💡 Recommendations for {args.repo}:")
            print("="*70)
            
            if not recommendations:
                print("No recommendations at this time. Your repository looks great! 🎉")
            else:
                for i, rec in enumerate(recommendations, 1):
                    priority_emoji = {
                        'high': '🔴',
                        'medium': '🟡',
                        'low': '🟢'
                    }.get(rec.get('priority', 'medium'), '🟡')
                    
                    print(f"\n{priority_emoji} {i}. {rec.get('title')}")
                    print(f"   Category: {rec.get('category')}")
                    print(f"   {rec.get('description')}")
                    print(f"   Action: {rec.get('action')}")
        
        elif args.command == 'improve':
            improvements = agent.suggest_improvements(args.repo)
            
            print(f"\n🚀 Improvement Plan for {args.repo}:")
            print("="*70)
            
            if improvements.get('quick_wins'):
                print("\n⚡ Quick Wins (Low Effort):")
                for rec in improvements['quick_wins']:
                    print(f"   • {rec.get('title')}")
            
            if improvements.get('high_priority'):
                print("\n🔴 High Priority:")
                for rec in improvements['high_priority']:
                    print(f"   • {rec.get('title')}")
            
            if improvements.get('medium_priority'):
                print("\n🟡 Medium Priority:")
                for rec in improvements['medium_priority']:
                    print(f"   • {rec.get('title')}")
            
            if improvements.get('low_priority'):
                print("\n🟢 Low Priority:")
                for rec in improvements['low_priority']:
                    print(f"   • {rec.get('title')}")
    
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

