from django.urls import path, include
from . import views

urlpatterns = [
    path('<int:user_pk>/<str:profile_slug>/<int:topic_pk>/<str:topic_slug>/<int:pk>/<str:slug>',
         include([
             path('', views.post_details, name='post_details'),
             # path('edit', views.PostEditView.as_view() name='post_edit'),
         ])),
    path('new', views.PostCreationView.as_view(), name='post_create')
]
