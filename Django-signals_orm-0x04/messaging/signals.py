from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    """Task 1: Create notification when a new message is created"""
    if created and not instance.notification_sent:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )
        instance.notification_sent = True
        instance.save(update_fields=['notification_sent'])


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """Task 2: Log message edits before saving"""
    if instance.pk:  # Only for existing messages
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:
                # Content changed, log to history
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_message.content
                )
                instance.edited = True
                instance.last_edited = timezone.now()
        except Message.DoesNotExist:
            pass


@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """Task 3: Clean up related data when user is deleted"""
    # Note: Using post_delete because CASCADE deletes will already handle
    # most relations. This is for any additional cleanup if needed.
    
    # Clear any cached data related to the user
    from django.core.cache import cache
    cache_keys = [
        f'user_messages_{instance.id}',
        f'user_conversations_{instance.id}',
        f'unread_count_{instance.id}',
    ]
    for key in cache_keys:
        cache.delete(key)