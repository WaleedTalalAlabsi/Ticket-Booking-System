#!/usr/bin/env python3
"""
Client startup script for Ticket Reservation System
"""

import sys
import os
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import tkinter
        import requests
        import urllib3
        print("✓ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_server_connection():
    """Check if server is running"""
    try:
        import requests
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        response = requests.get("https://localhost:8443/api/events", verify=False, timeout=5)
        if response.status_code == 200:
            print("✓ Server is running and accessible")
            return True
        else:
            print("✗ Server is not responding correctly")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to server")
        print("Make sure the server is running (python run_server.py)")
        return False
    except Exception as e:
        print(f"✗ Connection error: {e}")
        return False

def main():
    """Main function to start the client"""
    print("=" * 50)
    print("Ticket Reservation System - Client")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check server connection
    print("Checking server connection...")
    if not check_server_connection():
        print("\nTroubleshooting:")
        print("1. Make sure the server is running: python run_server.py")
        print("2. Check if the server is accessible at https://localhost:8443")
        print("3. For LAN access, update CLIENT_SERVER_URL in config.py")
        sys.exit(1)
    
    # Start client
    print("\nStarting client application...")
    print("=" * 50)
    
    try:
        subprocess.run([sys.executable, "client.py"], check=True)
    except KeyboardInterrupt:
        print("\nClient stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"Client error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
