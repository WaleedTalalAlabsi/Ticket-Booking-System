#!/usr/bin/env python3
"""
Test booking functionality specifically
"""

import requests
import urllib3
import json

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_booking():
    """Test the booking functionality"""
    base_url = "https://localhost:8443/api"
    
    # Login as admin
    print("1. Logging in as admin...")
    login_data = {"username": "admin", "password": "admin123"}
    response = requests.post(f"{base_url}/login", json=login_data, verify=False)
    
    if response.status_code != 200:
        print(f"❌ Login failed: {response.text}")
        return
    
    token = response.json()['token']
    headers = {'Authorization': f'Bearer {token}'}
    print("✅ Login successful")
    
    # Get events
    print("\n2. Getting events...")
    response = requests.get(f"{base_url}/events", verify=False)
    
    if response.status_code != 200:
        print(f"❌ Failed to get events: {response.text}")
        return
    
    events = response.json()
    print(f"✅ Found {len(events)} events")
    
    if not events:
        print("❌ No events available for testing")
        return
    
    # Test booking with first event
    event = events[0]
    print(f"\n3. Testing booking for event: {event['name']}")
    print(f"   Available tickets: {event['available_tickets']}")
    print(f"   Price per ticket: ${event['price_per_ticket']}")
    
    # Test booking with quantity 1
    booking_data = {
        "event_id": event['id'],
        "quantity": 1
    }
    
    print(f"\n4. Attempting to book {booking_data['quantity']} ticket(s)...")
    response = requests.post(f"{base_url}/bookings", json=booking_data, headers=headers, verify=False)
    
    print(f"   Response status: {response.status_code}")
    print(f"   Response body: {response.text}")
    
    if response.status_code == 201:
        print("✅ Booking successful!")
        booking = response.json()['booking']
        print(f"   Booking ID: {booking['id']}")
        print(f"   Total amount: ${booking['total_amount']}")
    else:
        print("❌ Booking failed!")
        error_data = response.json()
        print(f"   Error: {error_data.get('message', 'Unknown error')}")
    
    # Test booking with invalid quantity
    print(f"\n5. Testing with invalid quantity (0)...")
    booking_data['quantity'] = 0
    response = requests.post(f"{base_url}/bookings", json=booking_data, headers=headers, verify=False)
    print(f"   Response status: {response.status_code}")
    print(f"   Response body: {response.text}")
    
    # Test booking with negative quantity
    print(f"\n6. Testing with negative quantity (-1)...")
    booking_data['quantity'] = -1
    response = requests.post(f"{base_url}/bookings", json=booking_data, headers=headers, verify=False)
    print(f"   Response status: {response.status_code}")
    print(f"   Response body: {response.text}")

if __name__ == "__main__":
    test_booking()
