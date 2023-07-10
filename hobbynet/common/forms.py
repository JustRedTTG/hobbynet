from django import forms

from hobbynet.common.models import DISPLAY_NAME_ARGS, TITLE_ARGS


class TopicTitleFormRequired(forms.Form):
    title = forms.CharField(
        required=True,
        **TITLE_ARGS
    )

    class Meta:
        abstract = True


class DisplayNameForm(forms.Form):
    display_name = forms.CharField(
        required=False,
        **DISPLAY_NAME_ARGS
    )

    class Meta:
        abstract = True


class DisplayNameFormRequired(forms.Form):
    display_name = forms.CharField(
        required=True,
        **DISPLAY_NAME_ARGS
    )

    class Meta:
        abstract = True
