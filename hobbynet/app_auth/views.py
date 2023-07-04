import django.contrib.auth.views as auth_views
import django.contrib.auth.forms as auth_forms
from django import forms
from django.contrib.auth import get_user_model, login
from django.shortcuts import render
import django.views.generic as views
from django.urls import reverse_lazy

from hobbynet.profiles.models import Profile

UserModel = get_user_model()


class RegisterAccountForm(auth_forms.UserCreationForm):
    display_name = forms.CharField(max_length=20)


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


class RegisterAccountView(views.CreateView):
    template_name = 'app_auth/register.html'
    form_class = RegisterAccountForm
    success_url = reverse_lazy('profile_details_self')
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class LoginAccountView(auth_views.LoginView):
    template_name = 'app_auth/login.html'
