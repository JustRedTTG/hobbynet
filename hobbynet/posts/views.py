from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import FormView

from hobbynet.posts.forms import PostForm
from hobbynet.posts.models import Post
from hobbynet.topics.models import Topic

UserModel = get_user_model()


def post_details(request, user_pk, profile_slug, topic_pk, topic_slug, pk, slug):
    user = UserModel.objects.get(pk=user_pk)
    topic: Topic = user.topic_set.get(pk=topic_pk)
    post: Post = user.post_set.get(pk=pk)

    if not user or (
            request.user != user
            and
            not (request.user.is_superuser
                 or
                 (request.user.is_staff and request.user.has_perm('posts.view_post')))
            and
            post.visibility != 'public'
    ):
        raise Http404("Post doesn't exist")

    if user.profile.slug != profile_slug or topic.slug != topic_slug or post.slug != slug:
        return redirect(
            'post_details',
            user_pk=user.pk, profile_slug=user.profile.slug,
            topic_pk=topic.pk, topic_slug=topic.slug,
            pk=post.pk, slug=post.slug
        )

    return render(request, 'posts/post.html', {
        'post': user.post_set.get(id=pk)
    })


class PostCreationView(LoginRequiredMixin, FormView):
    form_class = PostForm
    template_name = 'base/post_create.html'

    def get_topic(self):
        topic_pk = self.request.GET.get('topic')
        return Topic.objects.get(pk=topic_pk) if topic_pk else None

    def get_initial(self):
        initial = {
            'user': self.request.user,
            'topic': self.get_topic()
        }
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topic'] = self.get_topic()
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        if not data['topic']:
            data['topic'] = form.initial['topic']

        post = self.request.user.post_set.create(**data)
        post.save()
        return redirect('profile_details_topic',
                        self.request.user.pk, self.request.user.profile.slug,
                        post.topic.pk, post.topic.slug)
