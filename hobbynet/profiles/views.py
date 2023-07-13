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
from django.views.generic import FormView, ListView

from hobbynet.common.forms import DisplayNameFormRequired, DisplayNameForm, TopicTitleFormRequired
from hobbynet.posts.models import Post
from hobbynet.profiles.models import Profile
from hobbynet.topics.models import Topic
from hobbynet.topics.forms import BasicTopicForm

UserModel: User = get_user_model()


class ProfileDetails(ListView):
    model = Post
    paginate_by = 2
    template_name = 'profiles/profile.html'
    context_object_name = 'posts'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user: UserModel = None
        self.topic: Topic = None

    def dispatch(self, request, *args, **kwargs):
        self.user = UserModel.objects.get(pk=kwargs.get('pk'))
        self.topic = self.user.topic_set.get(pk=kwargs.get('topic_pk')) if kwargs.get(
            'topic_pk') else self.user.topic_set.first()
        if not self.user or (
                self.request.user != self.user
                and
                not (self.request.user.is_superuser
                     or
                     (self.request.user.is_staff and self.request.user.has_perm('profiles.view_profile')))
                and
                self.user.profile.visibility != 'public'
        ):
            raise Http404("User profile doesn't exist")
        if self.user.profile.slug != self.kwargs.get('slug'):
            if self.topic:
                return redirect('profile_details_topic',
                                pk=self.user.pk, slug=self.user.profile.slug,
                                topic_pk=self.topic.pk, topic_slug=self.topic.slug)
            else:
                return redirect('profile_details', pk=self.user.pk, slug=self.user.profile.slug)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.user
        context['current_topic'] = self.topic
        return context

    def get_queryset(self):
        if self.topic:
            return self.topic.post_set.all().order_by('date_created').reverse()
        else:
            return Topic.objects.none()


class Editing(forms.ModelForm):
    class Meta:
        abstract = True
        model: any

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        change, delete = self.check_permissions()
        for field in self.fields.values():
            field.disabled = not change
            field.can_edit = change
        self.can_change = change
        self.can_delete = delete

    def check_permissions(self):
        editor = self.initial['editor']
        user = self.initial['user']
        if editor.is_superuser or editor == user:
            return [True] * 2
        if not editor.is_staff:
            return [False] * 2

        content_type = ContentType.objects.get_for_model(self.Meta.model)

        permission_change = f'{content_type.app_label}.change_{content_type.model}'
        permission_delete = f'{content_type.app_label}.delete{content_type.model}'

        return editor.has_perm(permission_change), editor.has_perm(permission_delete)


class ProfileForm(DisplayNameFormRequired, Editing, forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['display_name', 'profile_picture', 'visibility']


class TopicForm(Editing, BasicTopicForm, forms.ModelForm):
    class Meta(BasicTopicForm.Meta):
        pass


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
        edit_type, _, staff, _ = self.get_edit_information()
        if self.admin_selection and not self.request.user.is_superuser:
            if not staff or not self.request.user.has_perm(f'{edit_type}s.view_{edit_type}'):
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

            'editor': self.request.user,
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
