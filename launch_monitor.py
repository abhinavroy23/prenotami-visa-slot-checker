#!/usr/bin/env python3
"""
Simple launcher for the browser-based VISA monitor.
Opens Chrome with debug mode and starts monitoring.
"""

import subprocess
import time
import sys
import os

def start_chrome_debug():
    """Start Chrome in debug mode for Selenium connection."""
    print("🌐 Starting Chrome in debug mode...")
    
    # Chrome debug command for macOS
    chrome_cmd = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "--remote-debugging-port=9222",
        "--user-data-dir=/tmp/chrome-visa-debug",
        "--no-first-run",
        "--no-default-browser-check",
        "https://prenotami.esteri.it/"
    ]
    
    try:
        # Start Chrome in background
        process = subprocess.Popen(chrome_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)  # Give Chrome time to start
        
        print("✅ Chrome started successfully!")
        print("🔐 Please login to Prenotami in the browser window")
        print("📋 Navigate to Services page to confirm login")
        print()
        
        return process
        
    except FileNotFoundError:
        print("❌ Chrome not found at expected location")
        print("💡 Please install Google Chrome or update the path in the script")
        return None
    except Exception as e:
        print(f"❌ Failed to start Chrome: {str(e)}")
        return None

def main():
    print("🚀 VISA Monitor Launcher")
    print("=" * 30)
    print()
    
    # Start Chrome in debug mode
    chrome_process = start_chrome_debug()
    
    if not chrome_process:
        print("❌ Could not start Chrome")
        return
    
    # Wait for user to login
    input("Press Enter when you have logged in to Prenotami...")
    
    print()
    print("🎯 Starting VISA slot monitor...")
    print("🖥️ Keep both the browser window and this terminal open")
    print()
    
    # Start the monitor
    try:
        os.system("python3 browser_monitor.py")
    except KeyboardInterrupt:
        print("\n🛑 Monitor stopped")
    finally:
        print("🔒 Browser window left open for your use")

if __name__ == "__main__":
    main()
