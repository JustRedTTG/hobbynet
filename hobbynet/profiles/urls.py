from django.urls import path

from . import views

urlpatterns = [
    path('', views.profile_details_self, name='profile_details_self'),
    path('edit/', views.ProfileEdit.as_view(), name='profile_edit'),
    path('edit/<int:admin_selection>', views.ProfileEdit.as_view(), name='profile_edit_admin'),
    path('<int:pk>/<slug:slug>/', views.profile_details, name='profile_details'),
    path('<int:pk>/<slug:slug>/<int:topic_pk>/<slug:topic_slug>', views.profile_details, name='profile_details_topic'),
]