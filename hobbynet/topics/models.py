from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from django_backblaze_b2 import BackblazeB2Storage

from hobbynet.common.models import VisibilityRequired, profile_picture_class_generator, DisplayName, \
    TopicTitleRequired, Visibility, Description

UserModel = get_user_model()


def topic_image_generator(instance, filename):
    return f'topic_profile_pictures/{instance.user_id}/{filename}'


ProfilePictureMixin = profile_picture_class_generator(topic_image_generator)


class Topic(TopicTitleRequired, Description, DisplayName, ProfilePictureMixin, Visibility, models.Model):
    upload_to = topic_image_generator
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    def __repr__(self):
        return self.title

    def __str__(self):
        return self.title
