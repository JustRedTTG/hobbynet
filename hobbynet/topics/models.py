from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django_backblaze_b2 import BackblazeB2Storage

from hobbynet.common.models import VisibilityRequired, profile_picture_class_generator

UserModel = get_user_model()


def topic_image_generator(instance, filename):
    return f'topic_profile_pictures/{instance.user_id}_{instance.user.profile.slug}/{instance.id}/{filename}'


ProfilePictureMixin = profile_picture_class_generator(topic_image_generator, blank=True)


class Topic(ProfilePictureMixin, VisibilityRequired, models.Model):
    upload_to = topic_image_generator
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    title = models.CharField(max_length=20)
    display_name = models.CharField(max_length=20, null=True, blank=True)

    def __repr__(self):
        return self.title

    def __str__(self):
        return f'[{self.visibility}][{self.user}] {self.title}'
