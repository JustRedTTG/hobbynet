from django import forms

from .models import Post


class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].widget.attrs['placeholder'] = field_name.capitalize()
            self.fields[field_name].widget.attrs['autocomplete'] = 'off'
            self.fields[field_name].widget.attrs['class'] = f'w-100 form-control form-control-post form-control-post-{field_name} border-0'
        self.fields['content'].widget.attrs['class'] += ' auto-scroll-height'
        self.fields['content'].required = False
        self.fields['topic'].required = False

    class Meta:
        model = Post
        fields = ['topic', 'title', 'content', 'visibility', 'image']
