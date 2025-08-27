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
        print("Please run from: /Users/Abhinav.Roy2/Projects/others/prenotami-bot")
        return 1
    
    # Use the specific Python path
    python_path = "/Users/Abhinav.Roy2/.pyenv/versions/3.9.6/bin/python3"
    
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
