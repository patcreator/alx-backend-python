from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import models
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from .models import Message, Notification, MessageHistory


@login_required
def inbox(request):
    """Display user's inbox with unread messages"""
    # Task 4: Use custom manager for unread messages
    unread_messages = Message.unread_messages.for_user(request.user)
    
    # Optimize query with select_related
    all_messages = Message.objects.filter(
        receiver=request.user
    ).select_related('sender').only(
        'id', 'content', 'timestamp', 'read', 'sender__username', 'edited', 'edited_at'
    ).order_by('-timestamp')
    
    context = {
        'unread_messages': unread_messages,
        'all_messages': all_messages,
    }
    return render(request, 'messaging/inbox.html', context)


@cache_page(60)  # Task 5: Cache view for 60 seconds
@login_required
def conversation(request, user_id):
    """Display conversation between two users"""
    other_user = get_object_or_404(User, id=user_id)
    
    # Get messages between current user and other user
    messages = Message.objects.filter(
        models.Q(sender=request.user, receiver=other_user) |
        models.Q(sender=other_user, receiver=request.user)
    ).select_related('sender', 'receiver', 'edited_by').prefetch_related('replies').order_by('timestamp')
    
    # Mark messages as read when viewed
    Message.objects.filter(
        receiver=request.user,
        sender=other_user,
        read=False
    ).update(read=True)
    
    context = {
        'other_user': other_user,
        'messages': messages,
    }
    return render(request, 'messaging/conversation.html', context)


@login_required
def send_message(request, user_id):
    """Send a new message or reply"""
    if request.method == 'POST':
        receiver = get_object_or_404(User, id=user_id)
        content = request.POST.get('content', '').strip()
        parent_id = request.POST.get('parent_id')
        
        if content:
            message = Message.objects.create(
                sender=request.user,
                receiver=receiver,
                content=content,
                parent_message_id=parent_id if parent_id else None
            )
            
            # Clear conversation cache (Task 5)
            cache_key = f'conversation_{request.user.id}_{user_id}'
            cache.delete(cache_key)
            
        return redirect('conversation', user_id=user_id)
    return redirect('inbox')


@login_required
def delete_account(request):
    """Task 3: Delete user account with related data cleanup"""
    if request.method == 'POST':
        user = request.user
        
        # Logout user before deletion
        from django.contrib.auth import logout
        logout(request)
        
        # Delete user (this will trigger post_delete signal)
        user.delete()
        
        return redirect('login')
    
    return render(request, 'messaging/delete_account.html')


@login_required
def message_history(request, message_id):
    """Task 2: Display message edit history"""
    message = get_object_or_404(
        Message.objects.select_related('edited_by'),
        id=message_id
    )
    
    # Ensure user has permission to view this message's history
    if message.sender != request.user and message.receiver != request.user:
        return redirect('inbox')
    
    history = MessageHistory.objects.filter(
        message=message
    ).select_related('edited_by').order_by('-changed_at')
    
    context = {
        'message': message,
        'history': history,
    }
    return render(request, 'messaging/message_history.html', context)


@login_required
def edit_message(request, message_id):
    """Edit an existing message"""
    message = get_object_or_404(Message, id=message_id)
    
    # Ensure user is the sender
    if message.sender != request.user:
        return redirect('inbox')
    
    if request.method == 'POST':
        new_content = request.POST.get('content', '').strip()
        if new_content and new_content != message.content:
            # The pre_save signal will automatically log the old content
            message.content = new_content
            message.save()
            
            # Clear cache for this conversation
            cache_key = f'conversation_{request.user.id}_{message.receiver.id}'
            cache.delete(cache_key)
            
        return redirect('conversation', user_id=message.receiver.id)
    
    context = {
        'message': message,
    }
    return render(request, 'messaging/edit_message.html', context)