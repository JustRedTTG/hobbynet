from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.profile_details_self, name='profile_details_self'),
    path('<int:pk>/<slug:slug>/', include([
        path('', views.profile_details, name='profile_details'),
        # path('edit/', views.ProfileEdit.as_view()),
        # path('delete/', views.ProfileDelete.as_view()),
    ]))
]