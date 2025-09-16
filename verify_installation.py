#!/usr/bin/env python3
"""
Verification script for Ticket Reservation System
"""

import os
import sys
from pathlib import Path

def check_files():
    """Check if all required files exist"""
    required_files = [
        'server.py',
        'client.py', 
        'models.py',
        'config.py',
        'requirements.txt',
        'cert.pem',
        'key.pem',
        'instance/ticket_system.db'
    ]
    
    print("Checking required files...")
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - MISSING")
            missing_files.append(file)
    
    return len(missing_files) == 0

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'flask',
        'flask_sqlalchemy', 
        'flask_cors',
        'bcrypt',
        'jwt',
        'cryptography',
        'requests'
    ]
    
    print("\nChecking Python packages...")
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - NOT INSTALLED")
            missing_packages.append(package)
    
    return len(missing_packages) == 0

def check_ssl_certificates():
    """Check SSL certificate validity"""
    print("\nChecking SSL certificates...")
    
    try:
        from cryptography import x509
        from cryptography.hazmat.primitives import serialization
        
        # Check certificate
        with open('cert.pem', 'rb') as f:
            cert_data = f.read()
            cert = x509.load_pem_x509_certificate(cert_data)
            print(f"✓ Certificate valid until: {cert.not_valid_after}")
        
        # Check private key
        with open('key.pem', 'rb') as f:
            key_data = f.read()
            key = serialization.load_pem_private_key(key_data, password=None)
            print(f"✓ Private key loaded successfully")
        
        return True
    except Exception as e:
        print(f"✗ SSL certificate error: {e}")
        return False

def main():
    """Main verification function"""
    print("=" * 60)
    print("Ticket Reservation System - Installation Verification")
    print("=" * 60)
    
    all_good = True
    
    # Check files
    if not check_files():
        all_good = False
    
    # Check dependencies
    if not check_dependencies():
        all_good = False
        print("\nTo install missing packages, run:")
        print("pip install -r requirements.txt")
    
    # Check SSL certificates
    if not check_ssl_certificates():
        all_good = False
        print("\nTo regenerate SSL certificates, run:")
        print("python generate_certificates.py")
    
    print("\n" + "=" * 60)
    if all_good:
        print("🎉 INSTALLATION VERIFICATION PASSED!")
        print("The system is ready to use.")
        print("\nTo start the system:")
        print("1. Server: python run_server.py")
        print("2. Client: python run_client.py")
        print("\nDefault admin login: admin / admin123")
    else:
        print("❌ INSTALLATION VERIFICATION FAILED!")
        print("Please fix the issues above before using the system.")
        sys.exit(1)

if __name__ == "__main__":
    main()
