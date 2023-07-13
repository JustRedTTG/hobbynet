from django.urls import path, include
from . import views
from . import views

urlpatterns = [
    path('', include([
        path('<int:user_id>_<slug:profile_slug>/<int:topic_id>/<int:pk>',
             views.post_details, name='post_details'),
        path('new',
             views.PostCreationView.as_view(), name='post_create'),
        # path('<int:user_id>_<slug:profile_slug>/<int:topic_id>/edit',
        #      views.PostEditView.as_view(), name='post_edit')
    ]))
]