#!/bin/bash
# Quick start script for GitHub Repository Agent

echo "🚀 GitHub Repository Agent - Quick Start"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt --quiet

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies. Please check your Python/pip setup."
    exit 1
fi

echo "✅ Dependencies installed!"
echo ""
echo "🎯 Choose how to launch:"
echo "1. Web Interface (Recommended)"
echo "2. Command Line"
echo ""
read -p "Enter choice (1 or 2): " choice

if [ "$choice" == "1" ]; then
    echo ""
    echo "🌐 Starting web server..."
    echo "📍 Open http://localhost:5000 in your browser"
    echo "Press Ctrl+C to stop"
    echo ""
    python3 web_server.py
elif [ "$choice" == "2" ]; then
    echo ""
    echo "💻 Starting CLI..."
    python3 launch.py
else
    echo "❌ Invalid choice"
    exit 1
fi

