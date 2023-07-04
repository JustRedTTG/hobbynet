from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone


class UserModel(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(default=timezone.now)

class Profile(models.Model):
    user = models.OneToOneField(UserModel, related_name='profile', on_delete=models.CASCADE, primary_key=True)