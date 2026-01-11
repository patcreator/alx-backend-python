from django.urls import path
from .views import ChatMessageView, AdminView, TestView

urlpatterns = [
    path('messages/', ChatMessageView.as_view(), name='chat_messages'),
    path('admin-panel/', AdminView.as_view(), name='admin_panel'),
    path('test/', TestView.as_view(), name='test_middleware'),
]