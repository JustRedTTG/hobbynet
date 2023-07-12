from django.conf import settings
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, AnonymousUser
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.http import Http404, QueryDict
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from hobbynet.common.forms import DisplayNameFormRequired, DisplayNameForm, TopicTitleFormRequired
from hobbynet.profiles.models import Profile
from hobbynet.topics.models import Topic

UserModel: User = get_user_model()


def profile_details(request, pk, slug):
    user = UserModel.objects.get(pk=pk)
    if not user or (
            request.user != user
            and
            (not request.user.is_superuser
             or
             (not request.user.is_staff and request.user.has_perm('profiles_profile_view')))
            and
            user.profile.visibility != 'public'
    ):
        raise Http404("User profile doesn't exist")
    if user.profile.slug != slug:
        return redirect('profile_details', pk=pk, slug=user.profile.slug)
    return render(request, 'profiles/profile.html', context={
        'user': user,
    })


class ProfileForm(DisplayNameFormRequired, forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['display_name', 'profile_picture', 'visibility']


class TopicForm(TopicTitleFormRequired, DisplayNameForm, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["display_name"].widget.attrs['placeholder'] = self.initial['hint_topic_display_name']
        self.fields["display_name"].validators.append(self.validate_profile_display_name)

    def validate_profile_display_name(self, value):
        if value == self.initial['hint_topic_display_name']:
            raise ValidationError("The topic display name has to be different from the profile display name")

    def __iter__(self):
        for field_name, field in self.fields.items():
            field.can_edit = self.check_field_permissions(field_name)
            yield field_name, field

    def check_field_permissions(self, field_name):
        if self.fields.user.is_superuser:
            return True
        if not self.fields.user.is_staff:
            return False

        # Get the content type for the model associated with the form
        content_type = ContentType.objects.get_for_model(self.Meta.model)

        # Get the permission codename for the field
        permission_codename = f'{content_type.app_label}.change_{content_type.model}_{field_name}'

        # Check if the user has the required permission
        return self.fields.user.has_perm(permission_codename)

    class Meta:
        model = Topic
        fields = ['display_name', 'profile_picture', 'visibility', 'title']


class ProfileEdit(LoginRequiredMixin, FormView):
    """ This function will serve both the topic settings and profile settings,
    they are pretty similar, so we could manage with one common form,
    but also for profile will add extra stuff in the form"""
    # TODO: complete profile edit
    template_name = 'profiles/edit.html'

    def __init__(self, *args, **kwargs):
        self.admin_selection = None
        super().__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        self.admin_selection = int(kwargs.get('admin_selection', -1))
        self.admin_selection = self.admin_selection if self.admin_selection > 0 else None
        _, _, staff, _ = self.get_edit_information()
        if not staff and self.admin_selection:
            return redirect('profile_edit')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edit_type'], \
            context['topic_pk'], staff, context['edited_user'] = self.get_edit_information()
        if staff:
            context['users'] = UserModel.objects.all()
            context['admin_selection'] = self.admin_selection
        return context

    def get_edit_information(self):
        edit_type = self.request.GET.get('type', 'profile')
        topic = self.request.GET.get('topic', None)
        topic = int(topic) if topic else None
        staff = self.request.user.is_superuser or self.request.user.is_staff
        if not staff or not self.admin_selection:
            user = self.request.user
        else:
            try:
                user = UserModel.objects.get(pk=self.admin_selection)
            except UserModel.DoesNotExist:
                user = AnonymousUser()
                user.pk = self.admin_selection

        return edit_type, topic, staff, user

    def get_form_class(self):
        edit_type, _, _, _ = self.get_edit_information()
        if edit_type == 'profile':
            return ProfileForm
        elif edit_type == 'topic':
            return TopicForm

    def get_initial(self):
        edit_type, topic, _, user = self.get_edit_information()

        if edit_type == 'profile':
            base_object = user.profile
        elif edit_type == 'topic':
            base_object = user.topic_set.get(pk=topic)
        else:
            return {}

        base = {
            'display_name': base_object.display_name,
            'visibility': base_object.visibility,
            'profile_picture': base_object.profile_picture,

            'user': base_object.user,
            'pk': base_object.pk
        }

        if edit_type == 'profile':
            pass
        elif edit_type == 'topic':
            base['hint_topic_display_name'] = user.profile.display_name
            base['title'] = base_object.title

        return base

    def get_success_url(self):
        edit_type, _, _, user = self.get_edit_information()
        url = self.request.path  # Start with the current path

        # Check if the request has GET parameters
        if 'delete' in self.request.POST:
            if edit_type == 'profile':
                if user.pk != self.request.user.pk:
                    url = reverse_lazy('profile_edit')
                else:
                    url = reverse_lazy('goodbye')
            return url

        if self.request.GET:
            # Create a new QueryDict with the existing parameters
            params = self.request.GET.copy()
            params['success'] = '1'  # Add 'success' parameter

            # Append the updated query string to the URL
            url += '?' + params.urlencode()

        return url

    def form_valid(self, form: TopicForm):
        edit_type, _, _, _ = self.get_edit_information()
        form.instance.user = form.initial['user']
        pk = form.instance.pk = form.initial['pk']

        if edit_type == 'profile':
            obj = Profile.objects.get(pk=pk)
        elif edit_type == 'topic':
            obj = Topic.objects.get(pk=pk)
        else:
            obj = None
        if obj and obj.profile_picture:
            previous_profile_picture = obj.profile_picture
        else:
            previous_profile_picture = None

        if previous_profile_picture:
            if (not form.instance.profile_picture) or \
                    form.instance.profile_picture.name != previous_profile_picture.name:
                previous_profile_picture.delete(save=False)

        if 'delete' in self.request.POST:
            form.instance.delete()
        else:
            form.save()

        return super().form_valid(form)


@login_required
def profile_details_self(request):
    return redirect('profile_details', pk=request.user.pk, slug=request.user.profile.slug)
