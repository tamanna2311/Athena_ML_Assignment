#!/bin/bash

# Shark Tank Pitch Analyzer - Launch Script

echo "🦈 Welcome to the Shark Tank Pitch Analyzer!"
echo "==========================================="

# Ensure we are in the script's directory
cd "$(dirname "$0")"

# Check if python3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 could not be found. Please install Python 3."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment (venv)..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
if [ -f "requirements.txt" ]; then
    echo "⬇️  Checking and installing dependencies..."
    pip install -q -r requirements.txt
fi

# Set PYTHONPATH to current directory to avoid import errors
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Run the app
echo "🚀 Launching Streamlit App..."
echo "Press Ctrl+C to stop."
streamlit run app.py
