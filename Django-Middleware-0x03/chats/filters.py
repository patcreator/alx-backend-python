# messaging_app/chats/filters.py

import django_filters
from django_filters import rest_framework as filters
from .models import Message, Conversation
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageFilter(filters.FilterSet):
    # Filter by specific user (conversation with that user)
    with_user = filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        method='filter_with_user',
        label='Messages with specific user'
    )
    
    # Filter by date range
    start_date = filters.DateFilter(field_name='timestamp', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='timestamp', lookup_expr='lte')
    
    # Filter by read status
    is_read = filters.BooleanFilter(field_name='is_read')
    
    # Filter by sender or receiver
    sender = filters.ModelChoiceFilter(queryset=User.objects.all())
    receiver = filters.ModelChoiceFilter(queryset=User.objects.all())
    
    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'is_read', 'conversation']
    
    def filter_with_user(self, queryset, name, value):
        """
        Filter messages to show only those where the specified user 
        is either sender or receiver, and current user is the other participant.
        """
        user = self.request.user
        return queryset.filter(
            (Q(sender=user) & Q(receiver=value)) |
            (Q(sender=value) & Q(receiver=user))
        )