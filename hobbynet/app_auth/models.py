import re

import django.contrib.auth.models as auth_models
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.apps import apps

from hobbynet.profiles.models import Profile

EMAIL_REGEX = re.compile(r'^[\w.-]+@[\w.-]+\.\w+$')


class AccountManager(auth_models.BaseUserManager):
    def _create_user(self, email, password, display_name, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        if not password:
            raise ValueError("The given password must be set")

        if not EMAIL_REGEX.match(email):
            raise ValidationError('Invalid email format')

        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)

        profile = Profile(
            user=user,
            display_name=display_name
        )
        profile.save()

        return user

    def create_user(self, email, password=None, display_name=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, display_name, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class AccountModel(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    USERNAME_FIELD = 'email'
    email = models.EmailField(unique=True, blank=False, null=False)
    date_joined = models.DateTimeField(default=timezone.now)
    objects = AccountManager()

    is_staff = models.BooleanField(default=False)
