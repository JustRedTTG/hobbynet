from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()

class Topic(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    privacy = models.CharField(max_length=10, choices=getattr(settings, 'PRIVACY_MODEL_CHOICES', None))

    title = models.CharField(max_length=20)

    def __str__(self):
        return f'[{self.privacy}][{self.user}] {self.title}'