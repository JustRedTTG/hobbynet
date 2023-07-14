from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify

from hobbynet.common.models import Visibility, SLUG_MAX_LENGTH, TITLE_MAX_LENGTH, TopicTitleRequired
from hobbynet.topics.models import Topic
from pathlib import Path
from django_backblaze_b2 import BackblazeB2Storage

UserModel = get_user_model()


def posts_image_generator(instance, filename):
    return f'post_images/{instance.user_id}/{instance.topic_id}/{filename}'


class Post(TopicTitleRequired, Visibility, models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    date_created = models.DateTimeField(default=timezone.now)

    content = models.TextField(blank=True, null=True)
    image = models.ImageField(
        null=True,
        blank=True,
        storage=BackblazeB2Storage,
        upload_to=posts_image_generator
    )

    def save(self, *args, **kwargs):
        if not self.visibility:
            self.visibility = self.topic.visibility
        super().save(*args, **kwargs)

    def __repr__(self):
        return self.title

    def __str__(self):
        return f'[{self.visibility}/{self.topic.visibility}][{self.user}]'
