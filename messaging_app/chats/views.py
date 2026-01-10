from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from .models import User, Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter
import django_filters


# -------------------------------
# Conversation ViewSet
# -------------------------------
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]  # TASK 1: Apply custom permissions
    pagination_class = MessagePagination  # TASK 2: Add pagination

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with participants.
        Expects a list of user_ids in request.data['participants']
        """
        participants_ids = request.data.get('participants', [])
        if not participants_ids or len(participants_ids) < 1:
            return Response({"error": "Participants are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        conversation.participants.set(User.objects.filter(user_id__in=participants_ids))
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        """Override to show only conversations where user is a participant"""
        # Check what fields exist in the Conversation model
        if hasattr(Conversation, 'user1') and hasattr(Conversation, 'user2'):
            # If using user1/user2 model
            return Conversation.objects.filter(
                Q(user1=self.request.user) | 
                Q(user2=self.request.user)
            ).order_by('-created_at')
        elif hasattr(Conversation, 'participants'):
            # If using participants ManyToMany field
            return Conversation.objects.filter(
                participants=self.request.user
            ).order_by('-created_at')
        return super().get_queryset()


# -------------------------------
# Message ViewSet
# -------------------------------
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]  # TASK 1: Apply custom permissions
    pagination_class = MessagePagination  # TASK 2: Add pagination (20 messages per page)
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]  # TASK 2: Add filtering
    filterset_class = MessageFilter  # TASK 2: Add filtering

    def create(self, request, *args, **kwargs):
        """
        Send a message to an existing conversation.
        Expects:
        - request.data['conversation_id']
        - request.data['sender_id']
        - request.data['message_body']
        """
        conversation_id = request.data.get('conversation_id')
        sender_id = request.data.get('sender_id')
        message_body = request.data.get('message_body')

        if not conversation_id or not sender_id or not message_body:
            return Response({"error": "conversation_id, sender_id, and message_body are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
            sender = User.objects.get(user_id=sender_id)
            
            # TASK 1: Check if user is participant in conversation
            if not self._is_participant(conversation, request.user):
                return Response({"error": "You are not a participant in this conversation."},
                                status=status.HTTP_403_FORBIDDEN)
            
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found."}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"error": "Sender not found."}, status=status.HTTP_404_NOT_FOUND)

        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message_body=message_body
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        """Override to show only messages where user is a participant"""
        # Users can only see messages where they are sender or receiver
        # OR messages in conversations they're part of
        if hasattr(Message, 'sender') and hasattr(Message, 'receiver'):
            # If using sender/receiver model
            queryset = Message.objects.filter(
                Q(sender=self.request.user) | 
                Q(receiver=self.request.user)
            )
        elif hasattr(Message, 'conversation'):
            # If using conversation model
            # Get conversations where user is participant
            user_conversations = self._get_user_conversations(self.request.user)
            queryset = Message.objects.filter(
                conversation__in=user_conversations
            )
        else:
            queryset = super().get_queryset()
        
        return queryset.order_by('-timestamp')
    
    def _is_participant(self, conversation, user):
        """Helper to check if user is participant in conversation"""
        if hasattr(conversation, 'user1') and hasattr(conversation, 'user2'):
            return conversation.user1 == user or conversation.user2 == user
        elif hasattr(conversation, 'participants'):
            return conversation.participants.filter(id=user.id).exists()
        return False
    
    def _get_user_conversations(self, user):
        """Helper to get all conversations where user is a participant"""
        if hasattr(Conversation, 'user1') and hasattr(Conversation, 'user2'):
            return Conversation.objects.filter(
                Q(user1=user) | Q(user2=user)
            )
        elif hasattr(Conversation, 'participants'):
            return Conversation.objects.filter(participants=user)
        return Conversation.objects.none()