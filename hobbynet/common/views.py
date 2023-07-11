from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
import django.views.generic as views
from django.shortcuts import render

UserModel = get_user_model()


class HomeView(LoginRequiredMixin, views.ListView):
    model = UserModel
    template_name = 'common/home.html'


def goodbye(request):
    return render(request, 'common/goodbye.html')