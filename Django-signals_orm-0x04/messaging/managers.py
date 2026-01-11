from django.db import models
from django.contrib.auth.models import User


class UnreadMessagesManager(models.Manager):
    """Custom manager for unread messages (Task 4)"""
    
    def get_queryset(self):
        """Override default queryset to only include unread messages"""
        return super().get_queryset().filter(read=False)
    
    def unread_for_user(self, user):
        """Get unread messages for a specific user"""
        return self.get_queryset().filter(receiver=user)
    
    def mark_as_read(self, user, message_ids=None):
        """Mark messages as read for a user"""
        queryset = self.get_queryset().filter(receiver=user)
        if message_ids:
            queryset = queryset.filter(id__in=message_ids)
        return queryset.update(read=True)


class MessageQuerySet(models.QuerySet):
    """Custom QuerySet for Message model"""
    
    def unread(self):
        """Filter to only unread messages"""
        return self.filter(read=False)
    
    def for_user(self, user):
        """Filter messages for a specific user (either sender or receiver)"""
        return self.filter(models.Q(sender=user) | models.Q(receiver=user))
    
    def only_essential_fields(self):
        """Optimize query by selecting only necessary fields"""
        return self.only(
            'id', 
            'content', 
            'timestamp', 
            'read', 
            'sender__username',
            'receiver__username',
            'edited',
            'edited_at'
        )