from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Message, Notification, MessageHistory


class MessagingTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='test123')
        self.user2 = User.objects.create_user(username='user2', password='test123')
    
    def test_message_creation(self):
        """Test message creation and notification signal"""
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Hello, User2!"
        )
        
        # Check if message was created
        self.assertEqual(Message.objects.count(), 1)
        
        # Check if notification was created (Task 1)
        self.assertTrue(message.notification_sent)
        self.assertEqual(Notification.objects.count(), 1)
        self.assertEqual(Notification.objects.first().user, self.user2)
    
    def test_message_edit_history(self):
        """Test message edit history logging (Task 2)"""
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Original message"
        )
        
        # Edit the message
        message.content = "Edited message"
        message.save()
        
        # Check if history was created
        self.assertEqual(MessageHistory.objects.count(), 1)
        self.assertTrue(message.edited)
    
    def test_unread_messages_manager(self):
        """Test custom manager for unread messages (Task 4)"""
        # Create read and unread messages
        Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Read message",
            read=True
        )
        Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Unread message",
            read=False
        )
        
        # Test custom manager
        unread_count = Message.unread_messages.for_user(self.user2).count()
        self.assertEqual(unread_count, 1)
    
    def test_threaded_conversations(self):
        """Test threaded conversations (Task 3)"""
        parent = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Parent message"
        )
        
        reply = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content="Reply message",
            parent_message=parent
        )
        
        # Test relationship
        self.assertEqual(parent.replies.count(), 1)
        self.assertEqual(reply.parent_message, parent)
    
    def test_user_deletion_signal(self):
        """Test user deletion cleanup (Task 3)"""
        # Create messages
        Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Test message"
        )
        
        # Delete user
        self.user1.delete()
        
        # Check if messages are deleted (CASCADE should handle this)
        messages_from_user1 = Message.objects.filter(sender=self.user1)
        self.assertEqual(messages_from_user1.count(), 0)