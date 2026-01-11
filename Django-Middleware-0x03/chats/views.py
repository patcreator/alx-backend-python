from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Message, ChatRoom
import json


@method_decorator(csrf_exempt, name='dispatch')
class ChatMessageView(View):
    """View for handling chat messages."""
    
    def get(self, request):
        """Get all messages."""
        messages = Message.objects.all().values('user__username', 'content', 'created_at', 'role')
        return JsonResponse(list(messages), safe=False)
    
    def post(self, request):
        """Create a new message."""
        try:
            data = json.loads(request.body)
            user = request.user
            
            # Create a default chat room if none exists
            chat_room, created = ChatRoom.objects.get_or_create(
                name="General",
                defaults={'description': 'General chat room'}
            )
            
            # Create message
            message = Message.objects.create(
                chat_room=chat_room,
                user=user,
                content=data.get('content', ''),
                role=data.get('role', 'user')
            )
            
            return JsonResponse({
                'id': message.id,
                'user': message.user.username,
                'content': message.content,
                'created_at': message.created_at.isoformat(),
                'role': message.role
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


class AdminView(View):
    """Admin-only view."""
    
    def get(self, request):
        """Admin dashboard data."""
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        # Check if user has admin role (simplified check)
        if hasattr(request.user, 'is_staff') and request.user.is_staff:
            return JsonResponse({
                'message': 'Welcome to admin panel',
                'stats': {
                    'total_messages': Message.objects.count(),
                    'total_users': 1,  # Simplified
                }
            })
        else:
            return JsonResponse({'error': 'Admin access required'}, status=403)