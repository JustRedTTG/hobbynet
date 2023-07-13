from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import FormView

from hobbynet.posts.forms import PostForm
from hobbynet.topics.models import Topic

UserModel = get_user_model()


def post_details(request, user_id, profile_slug, topic_id, pk):
    user = UserModel.objects.get(id=user_id)

    return render(request, 'posts/post.html', {
        'post': user.post_set.get(id=pk)
    })


class PostCreationView(LoginRequiredMixin, FormView):
    form_class = PostForm
    template_name = 'base/post_create.html'

    def get_initial(self):
        initial = super().get_initial()
        topic_pk = self.request.GET.get('topic')
        initial['topic'] = Topic.objects.get(pk=topic_pk) if topic_pk else None
        return initial

    def form_valid(self, form):
        post = self.request.user.post_set.create(**form.cleaned_data)
        post.save()
        return redirect('profile_details_topic',
                        self.request.user.pk, self.request.user.profile.slug,
                        post.topic.pk, post.topic.slug)