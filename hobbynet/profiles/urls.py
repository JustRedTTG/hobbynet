from django.urls import path

from . import views

urlpatterns = [
    path('', views.profile_details_self, name='profile_details_self'),
    path('edit/', views.ProfileEdit.as_view(), name='profile_edit'),
    path('<int:pk>/<slug:slug>/', views.profile_details, name='profile_details'),
]