#!/usr/bin/env python3
"""
Installation script for Ticket Reservation System
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("✗ Python 3.7 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("\n" + "="*50)
    print("Installing Dependencies")
    print("="*50)
    
    # Check if pip is available
    if not run_command("pip --version", "Checking pip"):
        print("✗ pip is not available. Please install pip first.")
        return False
    
    # Install requirements
    if not run_command("pip install -r requirements.txt", "Installing Python packages"):
        return False
    
    return True

def generate_ssl_certificates():
    """Generate SSL certificates"""
    print("\n" + "="*50)
    print("Generating SSL Certificates")
    print("="*50)
    
    if not run_command("python generate_certificates.py", "Generating SSL certificates"):
        return False
    
    return True

def initialize_database():
    """Initialize the database"""
    print("\n" + "="*50)
    print("Initializing Database")
    print("="*50)
    
    if not run_command("python server.py --init-db", "Initializing database"):
        return False
    
    return True

def create_desktop_shortcuts():
    """Create desktop shortcuts for Windows"""
    if sys.platform == "win32":
        print("\n" + "="*50)
        print("Creating Desktop Shortcuts")
        print("="*50)
        
        try:
            import winshell
            from win32com.client import Dispatch
            
            desktop = winshell.desktop()
            
            # Server shortcut
            server_shortcut = os.path.join(desktop, "Ticket Server.lnk")
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(server_shortcut)
            shortcut.Targetpath = sys.executable
            shortcut.Arguments = os.path.join(os.getcwd(), "run_server.py")
            shortcut.WorkingDirectory = os.getcwd()
            shortcut.IconLocation = sys.executable
            shortcut.save()
            
            # Client shortcut
            client_shortcut = os.path.join(desktop, "Ticket Client.lnk")
            shortcut = shell.CreateShortCut(client_shortcut)
            shortcut.Targetpath = sys.executable
            shortcut.Arguments = os.path.join(os.getcwd(), "run_client.py")
            shortcut.WorkingDirectory = os.getcwd()
            shortcut.IconLocation = sys.executable
            shortcut.save()
            
            print("✓ Desktop shortcuts created")
            return True
        except ImportError:
            print("! Desktop shortcuts require additional packages (winshell, pywin32)")
            print("  Install with: pip install winshell pywin32")
            return False
        except Exception as e:
            print(f"! Could not create desktop shortcuts: {e}")
            return False
    else:
        print("! Desktop shortcuts are only available on Windows")
        return True

def main():
    """Main installation function"""
    print("="*60)
    print("Ticket Reservation System - Installation")
    print("="*60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n✗ Installation failed at dependency installation")
        sys.exit(1)
    
    # Generate SSL certificates
    if not generate_ssl_certificates():
        print("\n✗ Installation failed at SSL certificate generation")
        sys.exit(1)
    
    # Initialize database
    if not initialize_database():
        print("\n✗ Installation failed at database initialization")
        sys.exit(1)
    
    # Create desktop shortcuts (Windows only)
    create_desktop_shortcuts()
    
    print("\n" + "="*60)
    print("Installation Completed Successfully!")
    print("="*60)
    print("\nNext Steps:")
    print("1. Start the server: python run_server.py")
    print("2. Start the client: python run_client.py")
    print("3. Or use the batch files: start_server.bat and start_client.bat")
    print("\nDefault admin credentials:")
    print("Username: admin")
    print("Password: admin123")
    print("\nFor LAN setup, see NETWORK_SETUP.md")

if __name__ == "__main__":
    main()
