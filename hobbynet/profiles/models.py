from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.text import slugify

from hobbynet.common.models import VisibilityRequired, profile_picture_class_generator, DisplayNameRequired, \
    SLUG_MAX_LENGTH

UserModel = get_user_model()
DISPLAY_NAME_MIN_LENGTH = 6


def profile_image_generator(instance, filename):
    return f'user_profile_pictures/{instance.user_id}/{filename}'


ProfilePictureMixin = profile_picture_class_generator(profile_image_generator)


class Profile(DisplayNameRequired, ProfilePictureMixin, VisibilityRequired, models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, primary_key=True)

    @property
    def slug(self):
        return slugify(self.display_name)[:SLUG_MAX_LENGTH]

    def __str__(self):
        return self.display_name

    def delete(self, using=None, keep_parents=False):
        return self.user.delete(using, keep_parents)
