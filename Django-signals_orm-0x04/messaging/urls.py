from django.urls import path
from . import views

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('unread-only/', views.unread_only_inbox, name='unread_only_inbox'),  # Changed
    path('mark-all-read/', views.mark_all_as_read, name='mark_all_read'),
    path('conversation/<int:user_id>/', views.conversation, name='conversation'),
    path('send/<int:user_id>/', views.send_message, name='send_message'),
    path('delete-user/', views.delete_user, name='delete_user'),
    path('message-history/<int:message_id>/', views.message_history, name='message_history'),
    path('edit-message/<int:message_id>/', views.edit_message, name='edit_message'),
    path('test-manager/', views.test_custom_manager, name='test_manager'),
    path('display-history/<int:message_id>/', views.display_message_history, name='display_history'),
    
]