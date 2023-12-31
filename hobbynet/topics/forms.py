from django import forms
from django.core.exceptions import ValidationError

from hobbynet.common.forms import DisplayNameForm, TopicTitleFormRequired, DescriptionForm, Styling
from hobbynet.topics.models import Topic


class BasicTopicForm(Styling, TopicTitleFormRequired, DescriptionForm, DisplayNameForm, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["display_name"].widget.attrs['placeholder'] = self.initial.get('hint_topic_display_name', '')
        self.fields["display_name"].validators.append(self.validate_profile_display_name)
        self.fields['visibility'].required = False
        self.fields['visibility'].widget.choices[0] = ('', 'From Profile')
        self.fields['visibility'].initial = self.fields['visibility'].widget.choices[0][0]

    def validate_profile_display_name(self, value):
        if value == self.initial.get('hint_topic_display_name', ''):
            raise ValidationError("The topic display name has to be different from the profile display name")

    class Meta:
        model = Topic
        fields = ['description', 'display_name', 'profile_picture', 'visibility', 'title']
