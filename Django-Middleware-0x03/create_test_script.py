#!/usr/bin/env python
"""
Script to verify that the requests.log file exists and contains data.
"""
import os
import sys
import time
from datetime import datetime

def check_requests_log():
    """Check if requests.log file exists and contains data."""
    log_file = 'requests.log'
    
    print("=" * 60)
    print("Checking requests.log file...")
    print("=" * 60)
    
    # Check if file exists
    if not os.path.exists(log_file):
        print(f"❌ ERROR: {log_file} does not exist!")
        print("\nTo create the file, start the Django server and make requests:")
        print("1. python manage.py runserver")
        print("2. Open browser to: http://127.0.0.1:8000/chats/test/")
        print("3. Check if requests.log was created")
        return False
    
    # Check file size
    file_size = os.path.getsize(log_file)
    print(f"✓ File exists: {log_file}")
    print(f"✓ File size: {file_size} bytes")
    
    if file_size == 0:
        print("❌ WARNING: File exists but is empty!")
        print("\nMake some requests to the server to populate the log:")
        print("- http://127.0.0.1:8000/chats/test/")
        print("- http://127.0.0.1:8000/chats/messages/")
        print("- http://127.0.0.1:8000/chats/admin-panel/")
        return False
    
    # Read and display file content
    print("\n" + "=" * 60)
    print(f"Content of {log_file}:")
    print("=" * 60)
    
    try:
        with open(log_file, 'r') as f:
            content = f.read()
            print(content)
            
            # Count lines
            lines = content.strip().split('\n')
            non_empty_lines = [line for line in lines if line.strip()]
            print(f"\n✓ Total lines: {len(lines)}")
            print(f"✓ Non-empty lines: {len(non_empty_lines)}")
            
            if len(non_empty_lines) >= 3:  # Header + at least 2 log entries
                print("\n✅ SUCCESS: requests.log file exists and contains data!")
                return True
            else:
                print("\n⚠️  NOTE: File has minimal content. Make more requests.")
                return True
                
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False

def create_sample_requests():
    """Create sample requests to populate the log file."""
    print("\n" + "=" * 60)
    print("Creating sample requests...")
    print("=" * 60)
    
    import requests
    
    base_url = "http://127.0.0.1:8000"
    endpoints = [
        "/chats/test/",
        "/chats/messages/",
        "/admin/",
        "/chats/admin-panel/"
    ]
    
    for endpoint in endpoints:
        try:
            url = base_url + endpoint
            print(f"Requesting: {url}")
            response = requests.get(url, timeout=2)
            print(f"  Status: {response.status_code}")
            time.sleep(0.5)
        except requests.exceptions.ConnectionError:
            print(f"  ❌ Server not running at {base_url}")
            print("\nPlease start the server first:")
            print("python manage.py runserver")
            break
        except Exception as e:
            print(f"  ❌ Error: {e}")

if __name__ == "__main__":
    # First check the file
    if not check_requests_log():
        # Ask if user wants to create sample requests
        print("\n" + "=" * 60)
        user_input = input("Do you want to create sample requests? (y/n): ")
        if user_input.lower() == 'y':
            create_sample_requests()
            print("\nWaiting 2 seconds for logs to be written...")
            time.sleep(2)
            print("\n" + "=" * 60)
            check_requests_log()
    
    print("\n" + "=" * 60)
    print("Verification Complete!")
    print("=" * 60)