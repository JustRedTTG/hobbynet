from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginAccountView.as_view(), name='login'),
    path('register/', views.RegisterAccountView.as_view(), name='register'),
]
