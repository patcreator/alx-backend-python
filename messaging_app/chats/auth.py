"""
Custom authentication classes for the messaging app.
"""
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication that also validates user is active.
    """
    def authenticate(self, request):
        try:
            # Get the authentication result from parent class
            auth_result = super().authenticate(request)
            
            if auth_result is not None:
                user, token = auth_result
                
                # Check if user is active
                if not user.is_active:
                    raise AuthenticationFailed('User account is disabled.')
                
                return user, token
        except Exception as e:
            raise AuthenticationFailed(f'Authentication failed: {str(e)}')
        
        return None