from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

from hobbynet.common.models import VisibilityRequired, profile_picture_class_generator

UserModel = get_user_model()


def profile_image_generator(instance, filename):
    return f'user_profile_pictures/{instance.user_id}_{instance.slug}/{filename}'


ProfilePictureMixin = profile_picture_class_generator(profile_image_generator)


class Profile(ProfilePictureMixin, VisibilityRequired, models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, primary_key=True)
    display_name = models.CharField(max_length=20, null=True)

    @property
    def slug(self):
        return slugify(self.display_name.strip().lower())

    def __str__(self):
        return self.display_name
