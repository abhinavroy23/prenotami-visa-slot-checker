#!/bin/bash
# Browser Monitor Launcher
# Ensures correct Python environment and runs the monitor

echo "🎯 VISA Slot Monitor Launcher"
echo "=============================="
echo ""

# Check if we're in the right directory
if [ ! -f "browser_monitor.py" ]; then
    echo "❌ Error: browser_monitor.py not found"
    echo "Please run this script from the project directory"
    exit 1
fi

# Try to find Python 3 automatically
PYTHON_PATH=""
for candidate in python3 /usr/local/bin/python3 /opt/homebrew/bin/python3 /usr/bin/python3; do
    if command -v "$candidate" >/dev/null 2>&1; then
        if $candidate --version 2>&1 | grep -q "Python 3"; then
            PYTHON_PATH="$candidate"
            break
        fi
    fi
done

if [ -z "$PYTHON_PATH" ]; then
    echo "❌ Error: Python 3 not found"
    echo "Please install Python 3 or ensure it's in your PATH"
    exit 1
fi

echo "🐍 Using Python: $PYTHON_PATH"
echo "📦 Checking dependencies..."

# Check if selenium is installed
if ! $PYTHON_PATH -c "import selenium" 2>/dev/null; then
    echo "⚠️  Selenium not found, installing dependencies..."
    echo "💡 Trying user installation to avoid externally-managed-environment error..."
    
    # Try user installation first
    if $PYTHON_PATH -m pip install --user -r requirements.txt 2>/dev/null; then
        echo "✅ Dependencies installed with --user flag"
    elif $PYTHON_PATH -m pip install --break-system-packages -r requirements.txt 2>/dev/null; then
        echo "✅ Dependencies installed with --break-system-packages"
    else
        echo "❌ Failed to install dependencies automatically"
        echo "💡 Please install manually:"
        echo "   $PYTHON_PATH -m pip install --user -r requirements.txt"
        echo "   OR"
        echo "   pip3 install --user selenium webdriver-manager python-dotenv"
        exit 1
    fi
else
    echo "✅ Dependencies OK"
fi

echo ""
echo "🚀 Starting VISA Monitor..."
echo ""

# Run the monitor
exec $PYTHON_PATH browser_monitor.py
