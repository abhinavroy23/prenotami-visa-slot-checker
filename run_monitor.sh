#!/bin/bash
# Browser Monitor Launcher
# Ensures correct Python environment and runs the monitor

echo "🎯 VISA Slot Monitor Launcher"
echo "=============================="
echo ""

# Check if we're in the right directory
if [ ! -f "browser_monitor.py" ]; then
    echo "❌ Error: browser_monitor.py not found"
    echo "Please run this script from the project directory:"
    echo "cd /Users/Abhinav.Roy2/Projects/others/prenotami-bot"
    exit 1
fi

# Set up Python environment
export PATH="/Users/Abhinav.Roy2/.pyenv/versions/3.9.6/bin:$PATH"
PYTHON_PATH="/Users/Abhinav.Roy2/.pyenv/versions/3.9.6/bin/python3"

echo "🐍 Using Python: $PYTHON_PATH"
echo "📦 Checking dependencies..."

# Check if selenium is installed
if ! $PYTHON_PATH -c "import selenium" 2>/dev/null; then
    echo "⚠️  Selenium not found, installing dependencies..."
    $PYTHON_PATH -m pip install -r requirements.txt
    echo "✅ Dependencies installed"
else
    echo "✅ Dependencies OK"
fi

echo ""
echo "🚀 Starting VISA Monitor..."
echo ""

# Run the monitor
exec $PYTHON_PATH browser_monitor.py
