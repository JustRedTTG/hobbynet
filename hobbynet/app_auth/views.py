import django.contrib.auth.views as auth_views

from django.contrib.auth import login, logout
from django.shortcuts import redirect
import django.views.generic as views
from django.urls import reverse_lazy

from .forms import RegisterAccountForm


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


def logout_view(request):
    logout(request)
    return redirect('login')
