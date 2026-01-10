from django.urls import path
from . import views

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('conversation/<int:user_id>/', views.conversation, name='conversation'),
    path('send/<int:user_id>/', views.send_message, name='send_message'),
    path('delete-user/', views.delete_user, name='delete_user'),  # Updated name
    path('message-history/<int:message_id>/', views.message_history, name='message_history'),
    path('edit-message/<int:message_id>/', views.edit_message, name='edit_message'),
]