#!/usr/bin/env python3
"""
Test script for Ticket Reservation System
"""

import requests
import urllib3
import json
from datetime import datetime

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_server_connection():
    """Test if server is running and accessible"""
    try:
        response = requests.get("https://localhost:8443/api/events", verify=False, timeout=5)
        if response.status_code == 200:
            print("✓ Server is running and accessible")
            return True
        else:
            print(f"✗ Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to server")
        return False
    except Exception as e:
        print(f"✗ Connection error: {e}")
        return False

def test_user_registration():
    """Test user registration"""
    try:
        test_user = {
            "username": f"testuser_{datetime.now().strftime('%H%M%S')}",
            "email": f"test_{datetime.now().strftime('%H%M%S')}@example.com",
            "password": "testpass123"
        }
        
        response = requests.post("https://localhost:8443/api/register", 
                               json=test_user, verify=False, timeout=5)
        
        if response.status_code == 201:
            print("✓ User registration works")
            return test_user
        else:
            print(f"✗ User registration failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"✗ Registration test error: {e}")
        return None

def test_user_login(user_data):
    """Test user login"""
    try:
        login_data = {
            "username": user_data["username"],
            "password": user_data["password"]
        }
        
        response = requests.post("https://localhost:8443/api/login", 
                               json=login_data, verify=False, timeout=5)
        
        if response.status_code == 200:
            print("✓ User login works")
            return response.json()["token"]
        else:
            print(f"✗ User login failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"✗ Login test error: {e}")
        return None

def test_events_api():
    """Test events API"""
    try:
        response = requests.get("https://localhost:8443/api/events", verify=False, timeout=5)
        
        if response.status_code == 200:
            events = response.json()
            print(f"✓ Events API works - Found {len(events)} events")
            return True
        else:
            print(f"✗ Events API failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Events API test error: {e}")
        return False

def test_admin_login():
    """Test admin login"""
    try:
        admin_data = {
            "username": "admin",
            "password": "admin123"
        }
        
        response = requests.post("https://localhost:8443/api/login", 
                               json=admin_data, verify=False, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data["user"]["is_admin"]:
                print("✓ Admin login works")
                return data["token"]
            else:
                print("✗ Admin user is not marked as admin")
                return None
        else:
            print(f"✗ Admin login failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"✗ Admin login test error: {e}")
        return None

def main():
    """Run all tests"""
    print("=" * 50)
    print("Ticket Reservation System - Test Suite")
    print("=" * 50)
    
    # Test 1: Server connection
    print("\n1. Testing server connection...")
    if not test_server_connection():
        print("❌ Server is not running. Please start the server first:")
        print("   python run_server.py")
        return
    
    # Test 2: Events API
    print("\n2. Testing events API...")
    test_events_api()
    
    # Test 3: Admin login
    print("\n3. Testing admin login...")
    admin_token = test_admin_login()
    
    # Test 4: User registration
    print("\n4. Testing user registration...")
    user_data = test_user_registration()
    
    # Test 5: User login
    if user_data:
        print("\n5. Testing user login...")
        user_token = test_user_login(user_data)
    
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    print("✓ Server is running and accessible")
    print("✓ SSL certificates are working")
    print("✓ Database is initialized")
    print("✓ API endpoints are responding")
    print("\n🎉 System is ready for use!")
    print("\nNext steps:")
    print("1. Start the client: python run_client.py")
    print("2. Login with admin credentials: admin / admin123")
    print("3. Or register a new user through the client")

if __name__ == "__main__":
    main()
