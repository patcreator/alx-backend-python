"""
URL configuration for Django-Middleware-0x03 project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chats/', include('chats.urls')),
]