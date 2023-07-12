from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.TopicCreate.as_view(), name='topic_create'),
]