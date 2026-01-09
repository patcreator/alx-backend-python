from rest_framework import serializers
from .models import User, Conversation, Message


# -------------------------------
# User Serializer
# -------------------------------
class UserSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(required=False)  # Optional, professional field

    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'nickname', 'email', 'phone_number', 'role', 'created_at']


# -------------------------------
# Message Serializer
# -------------------------------
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    message_summary = serializers.SerializerMethodField()  # Professional, derived field

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at', 'message_summary']

    def get_message_summary(self, obj):
        # Return first 50 chars of the message as a summary
        return obj.message_body[:50] if obj.message_body else ""


# -------------------------------
# Conversation Serializer
# -------------------------------
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    note = serializers.CharField(required=False)  # Optional text field

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages', 'note']
