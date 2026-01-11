# messaging_app/chats/views.py

from rest_framework import viewsets, permissions
from django.db.models import Q
from .models import Message, Conversation
from .permissions import IsMessageOwner, IsConversationParticipant
from .serializers import MessageSerializer, ConversationSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsMessageOwner]
    
    def get_queryset(self):
        return Message.objects.filter(
            Q(sender=self.request.user) | 
            Q(receiver=self.request.user)
        ).order_by('-timestamp')

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsConversationParticipant]
    
    def get_queryset(self):
        return Conversation.objects.filter(
            Q(user1=self.request.user) | 
            Q(user2=self.request.user)
        ).order_by('-updated_at')