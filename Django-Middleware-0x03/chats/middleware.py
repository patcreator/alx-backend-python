"""
Middleware implementations for the Django-Middleware-0x03 project.
This file contains custom middleware classes for logging, access restriction,
rate limiting, and role-based permissions.
"""
import os
import json
import logging
from datetime import datetime, time
from collections import defaultdict
from django.http import HttpResponseForbidden, JsonResponse
from django.core.cache import cache
import re


class RequestLoggingMiddleware:
    """
    Middleware for logging user requests to a file.
    Logs timestamp, user, and request path for each request.
    Creates and writes to 'requests.log' file.
    """
    
    def __init__(self, get_response):
        """Initialize the middleware."""
        self.get_response = get_response
        self.log_file_path = 'requests.log'
        self.setup_log_file()
    
    def setup_log_file(self):
        """Create the requests.log file if it doesn't exist."""
        # Create the file if it doesn't exist
        if not os.path.exists(self.log_file_path):
            with open(self.log_file_path, 'w') as f:
                f.write("# Request Logging Middleware Log\n")
                f.write(f"# Log started at: {datetime.now()}\n")
                f.write("# Format: Timestamp - User - Path\n")
                f.write("=" * 50 + "\n")
            print(f"Created log file: {self.log_file_path}")
    
    def __call__(self, request):
        """Process each request and log it to requests.log file."""
        # Get user info
        if request.user.is_authenticated:
            user = request.user.username
        else:
            user = 'Anonymous'
        
        # Create log entry
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - User: {user} - Path: {request.path} - Method: {request.method}\n"
        
        # Write to requests.log file
        try:
            with open(self.log_file_path, 'a') as f:
                f.write(log_entry)
            
            # Also print to console for debugging
            print(f"Logged: {log_entry.strip()}")
        except Exception as e:
            print(f"Error writing to log file: {e}")
        
        # Process the request
        response = self.get_response(request)
        
        # Log response status
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            response_log = f"{timestamp} - Response: {response.status_code} - Path: {request.path}\n"
            with open(self.log_file_path, 'a') as f:
                f.write(response_log)
        except Exception as e:
            print(f"Error logging response: {e}")
        
        return response


class RestrictAccessByTimeMiddleware:
    """
    Middleware that restricts access to the messaging app 
    during certain hours (9 PM to 6 AM).
    """
    
    def __init__(self, get_response):
        """Initialize the middleware."""
        self.get_response = get_response
    
    def __call__(self, request):
        """Check current time and restrict access if outside allowed hours."""
        current_time = datetime.now().time()
        start_time = time(21, 0)  # 9 PM
        end_time = time(6, 0)     # 6 AM
        
        # Check if current time is between 9 PM and 6 AM
        if (current_time >= start_time) or (current_time <= end_time):
            # Check if the request is for chat-related paths
            if request.path.startswith('/chats/'):
                # Log the blocked attempt
                log_entry = f"{datetime.now()} - Access BLOCKED - Time: {current_time} - Path: {request.path}\n"
                with open('requests.log', 'a') as f:
                    f.write(log_entry)
                
                return JsonResponse({
                    'error': 'Access restricted between 9 PM and 6 AM'
                }, status=403)
        
        # Continue processing if within allowed hours
        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware:
    """
    Middleware that detects and blocks offensive language in messages.
    Implements rate limiting: 5 messages per minute per IP address.
    """
    
    def __init__(self, get_response):
        """Initialize the middleware."""
        self.get_response = get_response
        # List of offensive words to detect (simplified example)
        self.offensive_words = [
            'badword', 'offensive', 'inappropriate', 'hate',
            'spam', 'abuse', 'harass'
        ]
        # Rate limiting storage
        self.ip_message_count = defaultdict(list)
    
    def __call__(self, request):
        """Check for offensive language and enforce rate limiting."""
        current_time = datetime.now()
        
        # Rate limiting: Check only for POST requests to messages endpoint
        if request.method == 'POST' and '/messages/' in request.path:
            ip_address = self.get_client_ip(request)
            
            # Clean old entries (older than 1 minute)
            self.clean_old_entries(ip_address, current_time)
            
            # Check if user has exceeded rate limit
            if len(self.ip_message_count[ip_address]) >= 5:
                # Log the rate limit violation
                log_entry = f"{datetime.now()} - Rate Limit EXCEEDED - IP: {ip_address} - Path: {request.path}\n"
                with open('requests.log', 'a') as f:
                    f.write(log_entry)
                
                return JsonResponse({
                    'error': 'Rate limit exceeded. Maximum 5 messages per minute.'
                }, status=429)
            
            # Add current request to count
            self.ip_message_count[ip_address].append(current_time)
            
            # Check for offensive language in POST data
            try:
                if request.body:
                    # Make a copy of the body to read it
                    body_copy = request.body.decode('utf-8')
                    data = json.loads(body_copy) if body_copy else {}
                    content = data.get('content', '').lower()
                    
                    # Check for offensive words
                    for word in self.offensive_words:
                        if word in content:
                            # Log offensive content detection
                            log_entry = f"{datetime.now()} - Offensive Content DETECTED - IP: {ip_address} - Word: {word}\n"
                            with open('requests.log', 'a') as f:
                                f.write(log_entry)
                            
                            return JsonResponse({
                                'error': f'Message contains inappropriate content. Please remove offensive language.'
                            }, status=400)
            except (json.JSONDecodeError, UnicodeDecodeError):
                pass  # Not JSON data, skip offensive language check
        
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        """Extract client IP address from request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR', 'unknown')
        return ip
    
    def clean_old_entries(self, ip_address, current_time):
        """Remove entries older than 1 minute."""
        one_minute_ago = current_time.timestamp() - 60
        self.ip_message_count[ip_address] = [
            timestamp for timestamp in self.ip_message_count[ip_address]
            if timestamp.timestamp() > one_minute_ago
        ]


class RolePermissionMiddleware:
    """
    Middleware that checks user's role before allowing access to specific actions.
    Only allows admin or moderator access to admin panel.
    """
    
    def __init__(self, get_response):
        """Initialize the middleware."""
        self.get_response = get_response
    
    def __call__(self, request):
        """Check user role for admin panel access."""
        # Check if the request is for admin panel
        if '/admin-panel/' in request.path:
            if not request.user.is_authenticated:
                # Log unauthorized access attempt
                log_entry = f"{datetime.now()} - UNAUTHORIZED ACCESS - Path: {request.path} - User: Not authenticated\n"
                with open('requests.log', 'a') as f:
                    f.write(log_entry)
                
                return JsonResponse({
                    'error': 'Authentication required'
                }, status=401)
            
            # Check if user has admin or moderator role
            # In a real application, you would check a proper role field
            # For this example, we'll check is_staff for admin and a custom attribute for moderator
            is_admin = hasattr(request.user, 'is_staff') and request.user.is_staff
            is_moderator = hasattr(request.user, 'is_moderator') and request.user.is_moderator
            
            if not (is_admin or is_moderator):
                # Log permission denied
                log_entry = f"{datetime.now()} - PERMISSION DENIED - Path: {request.path} - User: {request.user.username}\n"
                with open('requests.log', 'a') as f:
                    f.write(log_entry)
                
                return JsonResponse({
                    'error': 'Admin or moderator access required'
                }, status=403)
        
        response = self.get_response(request)
        return response