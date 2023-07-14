from django import forms

from .models import Post


class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].widget.attrs['placeholder'] = field_name.capitalize()
            self.fields[field_name].widget.attrs['autocomplete'] = 'off'
            self.fields[field_name].widget.attrs[
                'class'] = f'w-100 form-control form-control-post form-control-post-{field_name} border-0'
        self.fields['content'].widget.attrs['class'] += ' auto-scroll-height'
        self.fields['content'].required = False
        self.fields['visibility'].required = False
        self.fields['visibility'].widget.choices[0] = ('', 'From Topic')
        self.fields['visibility'].initial = self.fields['visibility'].widget.choices[0][0]
        self.fields['topic'].widget.choices.queryset = self.fields['topic'].choices.queryset.filter(
            user=self.initial['user'])

    class Meta:
        model = Post
        fields = ['topic', 'title', 'content', 'visibility', 'image']
