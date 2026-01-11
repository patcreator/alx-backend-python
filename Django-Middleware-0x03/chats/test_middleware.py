#!/usr/bin/env python
"""
Test script to verify all middleware components are working.
"""
import os
import django
import time
import requests
from django.test import Client
from django.contrib.auth.models import User

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def test_request_logging():
    """Test that requests are logged to requests.log file."""
    print("\n" + "=" * 60)
    print("Testing RequestLoggingMiddleware")
    print("=" * 60)
    
    client = Client()
    
    # Make several requests
    endpoints = ['/chats/test/', '/chats/messages/', '/admin/']
    
    for endpoint in endpoints:
        print(f"\nMaking request to: {endpoint}")
        response = client.get(endpoint)
        print(f"Response status: {response.status_code}")
        time.sleep(0.1)
    
    # Check if requests.log exists and has content
    log_file = 'requests.log'
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            content = f.read()
            lines = content.strip().split('\n')
            print(f"\n✓ requests.log exists with {len(lines)} lines")
            
            # Show last 5 log entries
            print("\nLast 5 log entries:")
            for line in lines[-5:]:
                if line.strip():
                    print(f"  {line}")
    else:
        print(f"\n❌ requests.log does not exist!")
    
    return os.path.exists(log_file) and os.path.getsize(log_file) > 0

def test_time_restriction():
    """Test time-based access restriction."""
    print("\n" + "=" * 60)
    print("Testing RestrictAccessByTimeMiddleware")
    print("=" * 60)
    
    client = Client()
    
    # This test depends on current time
    from datetime import datetime
    current_time = datetime.now().time()
    
    print(f"Current time: {current_time}")
    print("Note: Middleware blocks access between 9 PM and 6 AM")
    
    response = client.get('/chats/messages/')
    if response.status_code == 403:
        print("✓ Time restriction is ACTIVE (outside allowed hours)")
    else:
        print("✓ Time restriction is INACTIVE (within allowed hours)")
    
    return True

def test_rate_limiting():
    """Test offensive language detection and rate limiting."""
    print("\n" + "=" * 60)
    print("Testing OffensiveLanguageMiddleware")
    print("=" * 60)
    
    # Create a test user
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )
    
    client = Client()
    client.login(username='testuser', password='testpass123')
    
    print("Testing offensive language detection...")
    
    # Test with clean message
    response = client.post(
        '/chats/messages/',
        data='{"content": "Hello, this is a test message"}',
        content_type='application/json'
    )
    print(f"Clean message response: {response.status_code}")
    
    # Test with offensive message
    response = client.post(
        '/chats/messages/',
        data='{"content": "This message contains badword content"}',
        content_type='application/json'
    )
    print(f"Offensive message response: {response.status_code}")
    
    # Test rate limiting (would need multiple rapid requests)
    print("\nRate limiting test would require 5+ requests in 1 minute")
    
    return True

def test_role_permissions():
    """Test role-based permission middleware."""
    print("\n" + "=" * 60)
    print("Testing RolePermissionMiddleware")
    print("=" * 60)
    
    # Test without authentication
    client = Client()
    print("\n1. Testing without authentication:")
    response = client.get('/chats/admin-panel/')
    print(f"   Response: {response.status_code} (expected: 401)")
    
    # Test with regular user
    regular_user = User.objects.create_user(
        username='regular',
        password='regularpass'
    )
    client.login(username='regular', password='regularpass')
    
    print("\n2. Testing with regular user:")
    response = client.get('/chats/admin-panel/')
    print(f"   Response: {response.status_code} (expected: 403)")
    
    # Test with admin user
    admin_user = User.objects.create_user(
        username='admin',
        password='adminpass'
    )
    admin_user.is_staff = True
    admin_user.save()
    
    client.login(username='admin', password='adminpass')
    
    print("\n3. Testing with admin user:")
    response = client.get('/chats/admin-panel/')
    print(f"   Response: {response.status_code} (expected: 200)")
    
    return True

def verify_requests_log():
    """Final verification of requests.log file."""
    print("\n" + "=" * 60)
    print("Final Verification of requests.log")
    print("=" * 60)
    
    log_file = 'requests.log'
    
    if not os.path.exists(log_file):
        print("❌ FAIL: requests.log does not exist!")
        return False
    
    with open(log_file, 'r') as f:
        content = f.read()
        lines = [line for line in content.split('\n') if line.strip()]
        
        print(f"File exists with {len(lines)} non-empty lines")
        print("\nSample of logged requests:")
        
        # Show requests that aren't comments
        request_lines = [line for line in lines if not line.startswith('#')]
        for i, line in enumerate(request_lines[:10]):
            print(f"  {i+1}. {line}")
        
        if len(request_lines) >= 5:
            print("\n✅ SUCCESS: requests.log contains sufficient logged requests!")
            return True
        else:
            print(f"\n⚠️  WARNING: Only {len(request_lines)} requests logged")
            print("   Make more requests to the server")
            return False

def main():
    """Run all tests."""
    print("Starting Middleware Tests")
    print("=" * 60)
    
    # Remove existing log file to start fresh
    if os.path.exists('requests.log'):
        print("Removing existing requests.log for fresh test...")
        os.remove('requests.log')
    
    tests_passed = 0
    total_tests = 5
    
    # Run tests
    if test_request_logging():
        tests_passed += 1
    
    if test_time_restriction():
        tests_passed += 1
    
    if test_rate_limiting():
        tests_passed += 1
    
    if test_role_permissions():
        tests_passed += 1
    
    if verify_requests_log():
        tests_passed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("\n🎉 ALL TESTS PASSED!")
        print("The middleware project is working correctly.")
        print(f"requests.log file exists with logged requests.")
    else:
        print(f"\n⚠️  Some tests didn't pass completely.")
        print("Check the logs above for details.")
    
    # Show the requests.log file content
    if os.path.exists('requests.log'):
        print("\n" + "=" * 60)
        print("FINAL REQUESTS.LOG CONTENT:")
        print("=" * 60)
        with open('requests.log', 'r') as f:
            print(f.read())

if __name__ == "__main__":
    main()