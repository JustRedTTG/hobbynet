from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('hobbynet.app_auth.urls')),
    path('profiles/', include('hobbynet.profiles.urls')),
]
