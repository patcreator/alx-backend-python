# messaging_app/chats/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'messages', views.MessageViewSet, basename='message')
router.register(r'conversations', views.ConversationViewSet, basename='conversation')

urlpatterns = [
    path('', include(router.urls)),
]