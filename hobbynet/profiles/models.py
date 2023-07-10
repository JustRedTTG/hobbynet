from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

from hobbynet.common.models import VisibilityRequired, profile_picture_class_generator, DisplayNameRequired

UserModel = get_user_model()


def profile_image_generator(instance, filename):
    return f'user_profile_pictures/{instance.user_id}/{filename}'


ProfilePictureMixin = profile_picture_class_generator(profile_image_generator)


class Profile(DisplayNameRequired, ProfilePictureMixin, VisibilityRequired, models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, primary_key=True)

    @property
    def slug(self):
        return slugify(self.display_name.strip().lower())

    def __str__(self):
        return self.display_name
