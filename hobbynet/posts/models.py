from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from hobbynet.topics.models import Topic

UserModel = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    privacy = models.CharField(
        null=True, blank=True,
        max_length=10,
        choices=getattr(settings, 'PRIVACY_MODEL_CHOICES', None))

    title = models.CharField(max_length=50)
    content = models.TextField()
    image = models.ImageField(null=True, blank=True)  # TODO: Add upload_to (use a storage service)

    def save(self, *args, **kwargs):
        if not self.privacy:
            self.privacy = self.topic.privacy
        super().save(*args, **kwargs)

    def __str__(self):
        return f'[{self.privacy}/{self.topic.privacy}][{self.user}]'
