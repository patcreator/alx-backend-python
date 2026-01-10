# messaging_app/chats/pagination.py
from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    """
    TASK 2: Add pagination listing on the messages such that 
    the api fetches 20 messages per page.
    """
    page_size = 20  # 20 messages per page
    page_size_query_param = 'page_size'
    max_page_size = 100