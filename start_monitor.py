#!/usr/bin/env python3
"""
Wrapper script to ensure browser monitor runs with correct Python environment
"""
import sys
import os
import subprocess

def main():
    print("🎯 VISA Monitor Environment Wrapper")
    print("=" * 40)
    
    # Ensure we're in the right directory
    if not os.path.exists('browser_monitor.py'):
        print("❌ Error: browser_monitor.py not found")
        print("Please run from the project directory")
        return 1
    
    # Try to find Python 3 automatically
    python_candidates = [
        "python3",
        "/usr/local/bin/python3", 
        "/opt/homebrew/bin/python3",
        "/usr/bin/python3"
    ]
    
    python_path = None
    for candidate in python_candidates:
        try:
            result = subprocess.run([candidate, "--version"], capture_output=True, text=True)
            if result.returncode == 0 and "Python 3" in result.stdout:
                python_path = candidate
                break
        except FileNotFoundError:
            continue
    
    if not python_path:
        print("❌ Error: Python 3 not found")
        print("Please install Python 3 or ensure it's in your PATH")
        return 1
    
    print(f"🐍 Python: {python_path}")
    print(f"📁 Directory: {os.getcwd()}")
    
    # Check if selenium is available
    try:
        result = subprocess.run([python_path, "-c", "import selenium; print('✅ Selenium OK')"], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print("⚠️  Installing dependencies...")
            subprocess.run([python_path, "-m", "pip", "install", "-r", "requirements.txt"])
        else:
            print(result.stdout.strip())
    except Exception as e:
        print(f"❌ Environment check failed: {e}")
        return 1
    
    print("")
    print("🚀 Starting monitor...")
    print("")
    
    # Run the monitor with the correct Python
    os.execv(python_path, [python_path, "browser_monitor.py"])

if __name__ == "__main__":
    sys.exit(main())
