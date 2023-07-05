from django.contrib.auth import get_user_model
from django.shortcuts import render
import django.views.generic as views

UserModel = get_user_model()

class HomeView(views.ListView):
    model = UserModel
    template_name = 'common/home.html'