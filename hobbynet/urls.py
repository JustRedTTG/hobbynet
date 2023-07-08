from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('hobbynet.common.urls')),
    path('accounts/', include('hobbynet.app_auth.urls')),
    path('profiles/', include('hobbynet.profiles.urls')),
    path('topics/', include('hobbynet.topics.urls')),
    path('posts/', include('hobbynet.posts.urls')),
    path('', include('django_backblaze_b2.urls')),
]
