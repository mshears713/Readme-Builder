#!/bin/bash

# Project Forge - Streamlit UI Launch Script
# This script starts the Streamlit web interface for Project Forge

echo "🔨 Starting Project Forge Streamlit UI..."
echo ""

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "❌ Error: Streamlit is not installed"
    echo "Please run: pip install -r requirements.txt"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found"
    echo "Please create a .env file with your OPENAI_API_KEY"
    echo ""
fi

# Set Python path to include project root
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Launch Streamlit
echo "🚀 Launching Streamlit UI..."
echo "The application will open in your browser at http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run streamlit_app.py
