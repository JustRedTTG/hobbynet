from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from hobbynet.topics.models import Topic
from pathlib import Path
from django_backblaze_b2 import BackblazeB2Storage

UserModel = get_user_model()

def posts_image_generator(instance, filename):
    return f'posts/{instance.user_id}{instance.topic_id}{instance.id}{instance.user.profile.slug}/{filename}'

class Post(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    privacy = models.CharField(
        null=True, blank=True,
        max_length=10,
        choices=getattr(settings, 'PRIVACY_MODEL_CHOICES', None))

    date_created = models.DateTimeField(default=timezone.now)

    title = models.CharField(max_length=50)
    content = models.TextField()
    image = models.ImageField(
        null=True,
        blank=True,
        storage=BackblazeB2Storage,
        upload_to=posts_image_generator
    )

    def save(self, *args, **kwargs):
        if not self.privacy:
            self.privacy = self.topic.privacy
        super().save(*args, **kwargs)

    def __repr__(self):
        return self.title

    def __str__(self):
        return f'[{self.privacy}/{self.topic.privacy}][{self.user}]'
