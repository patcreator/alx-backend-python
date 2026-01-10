from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UnreadMessagesManager(models.Manager):
    """Custom manager for unread messages (Task 4)"""
    
    def get_queryset(self):
        return super().get_queryset().filter(read=False)
    
    def for_user(self, user):
        """Get unread messages for a specific user"""
        return self.filter(receiver=user)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Task 1: Notification related
    notification_sent = models.BooleanField(default=False)
    
    # Task 2: Edit tracking
    edited = models.BooleanField(default=False)
    last_edited = models.DateTimeField(null=True, blank=True)
    
    # Task 3: Threaded conversations
    parent_message = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    
    # Task 4: Read status
    read = models.BooleanField(default=False)
    
    # Managers
    objects = models.Manager()  # Default manager
    unread_messages = UnreadMessagesManager()  # Custom manager for unread messages
    
    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"
    
    class Meta:
        ordering = ['-timestamp']


class Notification(models.Model):
    """Task 1: Store notifications for new messages"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Notification for {self.user}: {self.message}"


class MessageHistory(models.Model):
    """Task 2: Store message edit history"""
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    changed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"History for Message {self.message.id}"
    
    class Meta:
        verbose_name_plural = "Message Histories"