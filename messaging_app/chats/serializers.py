from rest_framework import serializers
from rest_framework.serializers import ValidationError  # <-- add this
from .models import User, Conversation, Message


# -------------------------------
# User Serializer
# -------------------------------
class UserSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'nickname', 'email', 'phone_number', 'role', 'created_at']


# -------------------------------
# Message Serializer
# -------------------------------
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    message_summary = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at', 'message_summary']

    def get_message_summary(self, obj):
        return obj.message_body[:50] if obj.message_body else ""


# -------------------------------
# Conversation Serializer
# -------------------------------
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    note = serializers.CharField(required=False)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages', 'note']

    # Optional: professional validation example
    def validate_note(self, value):
        if value and len(value) > 200:
            raise ValidationError("Note cannot exceed 200 characters.")
        return value
