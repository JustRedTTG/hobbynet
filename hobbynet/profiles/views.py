from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import FormView

from hobbynet.common.models import DisplayNameFormRequired, DisplayNameForm, TopicTitleFormRequired

UserModel: User = get_user_model()


def profile_details(request, pk, slug):
    user = UserModel.objects.get(pk=pk)
    if not user or (
            request.user != user
            and
            user.profile.visibility != 'public'
    ):
        raise Http404("User profile doesn't exist")
    if user.profile.slug != slug:
        return redirect('profile_details', pk=pk, slug=user.profile.slug)
    return render(request, 'profiles/profile.html', context={
        'user': user,
    })


class ProfileForm(DisplayNameFormRequired, forms.Form):
    profile_picture = forms.ImageField(required=True)
    visibility = forms.ChoiceField(choices=getattr(settings, 'PRIVACY_MODEL_CHOICES', None), required=True)

    class Meta:
        model = 'profile'


class TopicForm(TopicTitleFormRequired, DisplayNameForm, forms.Form):
    profile_picture = forms.ImageField(required=False)
    visibility = forms.ChoiceField(choices=getattr(settings, 'PRIVACY_MODEL_CHOICES', None), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["display_name"].widget.attrs['placeholder'] = self.initial['hint_topic_display_name']
        self.fields["display_name"].validators.append(self.validate_profile_display_name)

    def validate_profile_display_name(self, value):
        if value == self.initial['hint_topic_display_name']:
            raise ValidationError("The topic display name has to be different from the profile display name")

    class Meta:
        model = 'topic'


class ProfileEdit(LoginRequiredMixin, FormView):
    """ This function will serve both the topic settings and profile settings,
    they are pretty similar, so we could manage with one common form,
    but also for profile will add extra stuff in the form"""
    # TODO: complete profile edit
    template_name = 'profiles/edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edit_type'], \
            context['topic_pk'] = self.get_edit_information()
        return context

    def get_edit_information(self):
        edit_type = self.request.GET.get('type', 'profile')
        topic = self.request.GET.get('topic', None)
        topic = int(topic) if topic else None
        return edit_type, topic

    def get_form_class(self):
        edit_type, topic = self.get_edit_information()
        if edit_type == 'profile':
            return ProfileForm
        elif edit_type == 'topic':
            return TopicForm

    def get_initial(self):
        edit_type, topic = self.get_edit_information()

        if edit_type == 'profile':
            base_object = self.request.user.profile
        elif edit_type == 'topic':
            base_object = self.request.user.topic_set.get(pk=topic)
        else:
            return {}

        base = {
            'display_name': base_object.display_name,
            'visibility': base_object.visibility,
            'profile_picture': base_object.profile_picture.url if base_object.profile_picture else base_object.profile_picture,
        }

        if edit_type == 'profile':
            pass
        elif edit_type == 'topic':
            base['hint_topic_display_name'] = self.request.user.profile.display_name
            base['title'] = base_object.title

        return base

    def get_success_url(self):
        url = self.request.path  # Start with the current path

        # Check if the request has GET parameters
        if self.request.GET:
            # Create a new QueryDict with the existing parameters
            params = self.request.GET.copy()
            params['success'] = '1'  # Add 'success' parameter

            # Append the updated query string to the URL
            url += '?' + params.urlencode()

        return url

    def form_valid(self, form):
        edit_type, topic = self.get_edit_information()
        a = super().form_valid(form)
        return a


@login_required
def profile_details_self(request):
    return redirect('profile_details', pk=request.user.pk, slug=request.user.profile.slug)
