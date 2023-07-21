from django import forms
from django.contrib.contenttypes.models import ContentType
from hobbynet.common.forms import DisplayNameFormRequired
from hobbynet.profiles.models import Profile
from hobbynet.topics.forms import BasicTopicForm


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
