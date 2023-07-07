from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django_backblaze_b2 import BackblazeB2Storage

UserModel = get_user_model()

def topic_image_generator(instance, filename):
    return f'topic_profile_pictures/{instance.user_id}_{instance.user.profile.slug}/{instance.id}/{filename}'

class Topic(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    privacy = models.CharField(max_length=10, choices=getattr(settings, 'PRIVACY_MODEL_CHOICES', None))

    title = models.CharField(max_length=20)
    display_name = models.CharField(max_length=20, null=True, blank=True)
    profile_picture = models.ImageField(
        null=True,
        blank=True,
        storage=BackblazeB2Storage,
        upload_to=topic_image_generator
    )

    def __repr__(self):
        return self.title

    def __str__(self):
        return f'[{self.privacy}][{self.user}] {self.title}'