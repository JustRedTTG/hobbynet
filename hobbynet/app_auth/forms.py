from profile import Profile

from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

from hobbynet.app_auth.models import EMAIL_REGEX
from hobbynet.common.forms import DisplayNameFormRequired
from hobbynet.profiles.models import Profile

import django.contrib.auth.forms as auth_forms

UserModel = get_user_model()


class RegisterAccountForm(DisplayNameFormRequired, auth_forms.UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].validators.append(RegexValidator(
            regex=EMAIL_REGEX,
            message='Enter a real email address.',
        ))

    def save(self, commit=True):
        user = super().save(commit)

        profile = Profile(
            user=user,
            display_name=self.cleaned_data['display_name']
        )

        if commit:
            profile.save()

        return user

    class Meta(auth_forms.UserCreationForm.Meta):
        model = UserModel
        fields = ('email',)
