#!/usr/bin/env python
"""
Test script to demonstrate middleware functionality.
"""
import os
import django
from django.test import Client
from django.contrib.auth.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def test_middleware():
    """Test the middleware implementations."""
    client = Client()
    
    print("Testing RequestLoggingMiddleware...")
    response = client.get('/chats/messages/')
    print(f"Response: {response.status_code}")
    
    print("\nTesting RolePermissionMiddleware...")
    response = client.get('/chats/admin-panel/')
    print(f"Response without auth: {response.status_code}")
    
    print("\nTesting OffensiveLanguageMiddleware...")
    # Create a user and login
    user = User.objects.create_user('testuser', 'test@example.com', 'password')
    user.is_staff = True
    user.save()
    client.login(username='testuser', password='password')
    
    print("\nAll middleware tests completed!")

if __name__ == '__main__':
    test_middleware()