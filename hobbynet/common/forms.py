from django import forms

from hobbynet.common.models import DISPLAY_NAME_ARGS, TITLE_ARGS, DESCRIPTION_ARGS


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


class DescriptionForm(forms.Form):
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'auto-scroll-height'}),
        **DESCRIPTION_ARGS
    )

    class Meta:
        abstract = True


class Styling(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = ' '.join(
                (self.fields[field_name].widget.attrs.get('class') or '', 'form-control'))

    class Meta:
        abstract = True


class DisplayNameFormRequired(forms.Form):
    display_name = forms.CharField(
        required=True,
        **DISPLAY_NAME_ARGS
    )

    class Meta:
        abstract = True
