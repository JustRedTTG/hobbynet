from django import forms
from django.core.exceptions import ValidationError

from hobbynet.common.forms import DisplayNameForm, TopicTitleFormRequired
from hobbynet.topics.models import Topic


class BasicTopicForm(TopicTitleFormRequired, DisplayNameForm, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["display_name"].widget.attrs['placeholder'] = self.initial.get('hint_topic_display_name', '')
        self.fields["display_name"].validators.append(self.validate_profile_display_name)

    def validate_profile_display_name(self, value):
        if value == self.initial.get('hint_topic_display_name', ''):
            raise ValidationError("The topic display name has to be different from the profile display name")

    class Meta:
        model = Topic
        fields = ['display_name', 'profile_picture', 'visibility', 'title']