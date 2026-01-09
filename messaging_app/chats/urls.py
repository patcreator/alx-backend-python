from rest_framework import routers
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet

# Create a router and register our viewsets
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversations')
router.register(r'messages', MessageViewSet, basename='messages')

# Include the router URLs in app-level urls
urlpatterns = [
    path('', include(router.urls)),
]
