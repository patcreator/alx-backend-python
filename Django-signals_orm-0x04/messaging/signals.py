from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
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
    if not instance.pk:
        return
    
    try:
        original = Message.objects.get(pk=instance.pk)
        if original.content != instance.content:
            MessageHistory.objects.create(
                message=instance,
                old_content=original.content,
                edited_by=instance.sender
            )
            instance.edited = True
            instance.edited_at = timezone.now()
            instance.edited_by = instance.sender
    except Message.DoesNotExist:
        pass


@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """Task 3: Clean up related data when user is deleted"""
    # First, let's manually delete related data to ensure foreign key constraints
    # This is in addition to CASCADE deletes
    
    # Delete messages where user is sender - using filter().delete()
    Message.objects.filter(sender=instance).delete()
    
    # Delete messages where user is receiver - using filter().delete()
    Message.objects.filter(receiver=instance).delete()
    
    # Delete notifications for the user - using filter().delete()
    Notification.objects.filter(user=instance).delete()
    
    # Delete MessageHistory where edited_by is this user
    MessageHistory.objects.filter(edited_by=instance).delete()
    
    # Clear cache
    from django.core.cache import cache
    cache_keys = [
        f'user_messages_{instance.id}',
        f'user_conversations_{instance.id}',
        f'unread_count_{instance.id}',
    ]
    for key in cache_keys:
        cache.delete(key)
    
    # Also delete any orphaned MessageHistory records
    # (those where the message was deleted but history remains)
    # This handles cases where CASCADE might not work as expected
    MessageHistory.objects.filter(
        message__isnull=True
    ).delete()


# Additional signal to handle User deletion with custom logic
@receiver(post_delete, sender=User)
def handle_user_deletion_cascade(sender, instance, **kwargs):
    """Alternative implementation showing manual cascade deletion"""
    # Get all related data before deletion
    user_messages = Message.objects.filter(
        models.Q(sender=instance) | models.Q(receiver=instance)
    )
    
    # Log deletion for audit
    print(f"User {instance.username} deleted. Cleaning up {user_messages.count()} messages.")
    
    # Manually trigger deletion - this ensures we respect foreign key constraints
    # by deleting in the right order
    try:
        # First delete notifications (they reference messages and user)
        Notification.objects.filter(user=instance).delete()
        
        # Then delete message history
        MessageHistory.objects.filter(edited_by=instance).delete()
        
        # Finally delete messages
        Message.objects.filter(sender=instance).delete()
        Message.objects.filter(receiver=instance).delete()
        
    except Exception as e:
        print(f"Error during user data cleanup: {e}")