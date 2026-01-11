from django.contrib import admin
from .models import Message, Notification, MessageHistory


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'timestamp', 'read', 'edited')
    list_filter = ('read', 'edited', 'timestamp')
    search_fields = ('content', 'sender__username', 'receiver__username')
    raw_id_fields = ('sender', 'receiver', 'parent_message')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'message', 'created_at', 'read')
    list_filter = ('read', 'created_at')
    search_fields = ('user__username', 'message__content')


@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'changed_at')
    search_fields = ('old_content', 'message__content')