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
            print("💡 Trying user installation to avoid externally-managed-environment error...")
            
            # Try user installation first (--user flag)
            try:
                result = subprocess.run([python_path, "-m", "pip", "install", "--user", "-r", "requirements.txt"], 
                                      capture_output=True, text=True, check=True)
                print("✅ Dependencies installed with --user flag")
            except subprocess.CalledProcessError:
                print("⚠️  User installation failed, trying with --break-system-packages...")
                try:
                    result = subprocess.run([python_path, "-m", "pip", "install", "--break-system-packages", "-r", "requirements.txt"], 
                                          capture_output=True, text=True, check=True)
                    print("✅ Dependencies installed with --break-system-packages")
                except subprocess.CalledProcessError as e:
                    print("❌ Failed to install dependencies")
                    print("💡 Please install manually:")
                    print(f"   {python_path} -m pip install --user -r requirements.txt")
                    print("   OR")
                    print("   pip3 install --user selenium webdriver-manager python-dotenv")
                    return 1
        else:
            print(result.stdout.strip())
    except Exception as e:
        print(f"❌ Environment check failed: {e}")
        print("💡 Try installing dependencies manually:")
        print(f"   {python_path} -m pip install --user selenium webdriver-manager python-dotenv")
        return 1
    
    print("")
    print("🚀 Starting monitor...")
    print("")
    
    # Get the full path for execv if needed
    if not os.path.isabs(python_path):
        # Find the full path for relative commands like "python3"
        import shutil
        full_python_path = shutil.which(python_path)
        if full_python_path:
            python_path = full_python_path
        else:
            # Fallback to subprocess if we can't resolve the path
            print(f"🔄 Using subprocess fallback for {python_path}")
            try:
                subprocess.run([python_path, "browser_monitor.py"])
                return 0
            except Exception as e:
                print(f"❌ Failed to start monitor: {e}")
                return 1
    
    # Run the monitor with the correct Python
    try:
        os.execv(python_path, [python_path, "browser_monitor.py"])
    except FileNotFoundError:
        # Final fallback
        print(f"🔄 Exec failed, using subprocess for {python_path}")
        try:
            subprocess.run([python_path, "browser_monitor.py"])
            return 0
        except Exception as e:
            print(f"❌ Failed to start monitor: {e}")
            return 1

if __name__ == "__main__":
    sys.exit(main())
