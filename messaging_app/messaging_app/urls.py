from django.contrib import admin
from django.urls import path, include
# messaging_app/urls.py
from django.http import JsonResponse

def home(request):
    return JsonResponse({"message": "Welcome to the Messaging API"})

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/v1/', include('chats.urls')),       # main API
    path('api-auth/', include('rest_framework.urls')),  # DRF login/logout
]
