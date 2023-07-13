from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from django_backblaze_b2 import BackblazeB2Storage

from hobbynet.common.models import VisibilityRequired, profile_picture_class_generator, DisplayName, TopicTitleRequired, \
    SLUG_MAX_LENGTH

UserModel = get_user_model()


def topic_image_generator(instance, filename):
    return f'topic_profile_pictures/{instance.user_id}/{filename}'


ProfilePictureMixin = profile_picture_class_generator(topic_image_generator, blank=True)


class Topic(TopicTitleRequired, DisplayName, ProfilePictureMixin, VisibilityRequired, models.Model):
    upload_to = topic_image_generator
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    def __repr__(self):
        return self.title

    def __str__(self):
        return f'[{self.visibility}][{self.user}] {self.title}'

    @property
    def slug(self):
        return slugify(self.title)[:SLUG_MAX_LENGTH]