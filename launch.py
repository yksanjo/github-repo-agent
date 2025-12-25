#!/usr/bin/env python3
"""
Quick launch script for GitHub Repository Agent.
Choose between CLI or Web interface.
"""

import sys
import subprocess
import os

def main():
    print("="*70)
    print("🚀 GitHub Repository Agent")
    print("="*70)
    print("\nChoose an option:")
    print("1. Web Interface (Recommended) - Open in browser")
    print("2. Command Line Interface")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == '1':
        print("\n🌐 Starting web server...")
        print("📍 Server will be available at: http://localhost:5000")
        print("💡 Open your browser and navigate to the URL above")
        print("🔒 No API keys needed - everything runs locally!")
        print("\nPress Ctrl+C to stop the server\n")
        try:
            from web_server import app
            app.run(debug=True, host='0.0.0.0', port=5000)
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped. Goodbye!")
        except ImportError:
            print("❌ Error: Flask not installed. Run: pip install -r requirements.txt")
    
    elif choice == '2':
        print("\n💻 Starting CLI...")
        print("="*70)
        subprocess.run([sys.executable, 'cli.py'] + sys.argv[1:])
    
    elif choice == '3':
        print("\n👋 Goodbye!")
        sys.exit(0)
    
    else:
        print("\n❌ Invalid choice. Please run again and select 1, 2, or 3.")

if __name__ == '__main__':
    main()

