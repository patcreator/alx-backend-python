from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('chats.urls')),       # main API
    path('api-auth/', include('rest_framework.urls')),  # DRF login/logout
]
