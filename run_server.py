#!/usr/bin/env python3
"""
Server startup script for Ticket Reservation System
"""

import sys
import os
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import flask
        import flask_sqlalchemy
        import flask_cors
        import bcrypt
        import jwt
        import cryptography
        import requests
        print("✓ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_ssl_certificates():
    """Check if SSL certificates exist"""
    cert_file = Path("cert.pem")
    key_file = Path("key.pem")
    
    if cert_file.exists() and key_file.exists():
        print("✓ SSL certificates found")
        return True
    else:
        print("✗ SSL certificates not found")
        print("Generating SSL certificates...")
        try:
            subprocess.run([sys.executable, "generate_certificates.py"], check=True)
            print("✓ SSL certificates generated successfully")
            return True
        except subprocess.CalledProcessError:
            print("✗ Failed to generate SSL certificates")
            return False

def main():
    """Main function to start the server"""
    print("=" * 50)
    print("Ticket Reservation System - Server")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check SSL certificates
    if not check_ssl_certificates():
        sys.exit(1)
    
    # Initialize database
    print("Initializing database...")
    try:
        subprocess.run([sys.executable, "server.py", "--init-db"], check=True)
        print("✓ Database initialized")
    except subprocess.CalledProcessError:
        print("✗ Failed to initialize database")
        sys.exit(1)
    
    # Start server
    print("\nStarting server...")
    print("Server will be available at:")
    print("- https://localhost:8443 (local access)")
    print("- https://<your-ip>:8443 (LAN access)")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        subprocess.run([sys.executable, "server.py"], check=True)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
