from django.db import models
from django.conf import settings


# Create your models here.

class Visibility(models.Model):
    visibility = models.CharField(
        null=True, blank=True,
        max_length=10,
        choices=getattr(settings, 'PRIVACY_MODEL_CHOICES', None))

    class Meta:
        abstract = True


class VisibilityRequired(models.Model):
    visibility = models.CharField(
        max_length=10,
        choices=getattr(settings, 'PRIVACY_MODEL_CHOICES', None))

    class Meta:
        abstract = True
