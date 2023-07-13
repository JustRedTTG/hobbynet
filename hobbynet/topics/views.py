from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from hobbynet.topics.forms import BasicTopicForm
from hobbynet.topics.models import Topic


# Create your views here.


class TopicCreate(LoginRequiredMixin, FormView):
    form_class = BasicTopicForm
    template_name = 'topics/create.html'



    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.create = True
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edit_type'] = 'topic'
        return context

    def get_initial(self):
        kwargs = super().get_initial()
        kwargs['hint_topic_display_name'] = self.request.user.profile.display_name
        return kwargs

    def form_valid(self, form):
        topic = self.request.user.topic_set.create(**form.cleaned_data)
        topic.save()
        return redirect('profile_details_topic',
                        self.request.user.pk, self.request.user.profile.slug,
                        topic.pk, topic.slug)
