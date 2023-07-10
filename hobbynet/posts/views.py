from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render


UserModel = get_user_model()


def post_details(request, user_id, profile_slug, topic_id, pk):
    user = UserModel.objects.get(id=user_id)

    return render(request, 'posts/post.html', {
        'post': user.post_set.get(id=pk)
    })

# class PostCreationView():
#     pass
#
#
# class PostEditView:
#     pass
