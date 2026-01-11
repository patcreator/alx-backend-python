from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

def home(request):
    return JsonResponse({"message": "Welcome to the Messaging API"})

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    
    # JWT Authentication URLs
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # DRF authentication URLs (for session auth in browsable API)
    path('api-auth/', include('rest_framework.urls')),
    
    # Main API
    path('api/v1/', include('chats.urls')),
]