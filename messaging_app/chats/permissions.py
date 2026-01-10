"""
Custom permissions for the messaging app.
"""
from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.
        return obj.owner == request.user


class IsMessageOwner(BasePermission):
    """
    Permission to only allow message owners to view/edit their own messages.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the requesting user is the sender or receiver of the message
        return obj.sender == request.user or obj.receiver == request.user


class IsConversationParticipant(BasePermission):
    """
    Permission to only allow conversation participants to view the conversation.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the requesting user is either user1 or user2 in the conversation
        return obj.user1 == request.user or obj.user2 == request.user


class IsUserProfileOwner(BasePermission):
    """
    Permission to only allow users to view/edit their own profile.
    """
    def has_object_permission(self, request, view, obj):
        # User can only access their own profile
        return obj == request.user


class IsAdminOrReadOnly(BasePermission):
    """
    Permission to allow admins full access and others read-only.
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to admin users
        return request.user and request.user.is_staff


class IsOwnerOrAdmin(BasePermission):
    """
    Permission to allow owners and admins full access.
    """
    def has_object_permission(self, request, view, obj):
        # Allow if user is owner or admin
        return obj.user == request.user or request.user.is_staff