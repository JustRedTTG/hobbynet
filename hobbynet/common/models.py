from django_extensions.db.fields import AutoSlugField
from django.core.validators import MinLengthValidator
from django.core.files.base import ContentFile
from django.conf import settings
from urllib.parse import quote
from django.db import models
import random

# Please note that altering these values
# requires a migration to be made.
SLUG_MAX_LENGTH = 30
NAME_MAX_LENGTH = 60
TITLE_MAX_LENGTH = 85

NAME_MIN_LENGTH = 5
TITLE_MIN_LENGTH = 5

DISPLAY_NAME_ARGS = {
    'max_length': NAME_MAX_LENGTH,
    'validators': [MinLengthValidator(NAME_MIN_LENGTH)]
}

TITLE_ARGS = {
    'max_length': TITLE_MAX_LENGTH,
    'validators': [MinLengthValidator(TITLE_MIN_LENGTH)]
}

DESCRIPTION_ARGS = {

}


def slugify(value):
    return quote(value.replace(' ', '-').replace('/', '-').replace('\\', '-'))


def create_slug_mixin(slug_field):
    class SlugMixin(models.Model):
        slug = AutoSlugField(
            populate_from=slug_field,
            slugify_function=slugify,
            max_length=SLUG_MAX_LENGTH,
            unique=False,
        )

        class Meta:
            abstract = True

    return SlugMixin


class Visibility(models.Model):
    visibility = models.CharField(
        default='private',
        blank=True,
        max_length=10,
        choices=getattr(settings, 'PRIVACY_MODEL_CHOICES', None))

    class Meta:
        abstract = True


class VisibilityRequired(models.Model):
    visibility = models.CharField(
        default='private',
        max_length=10,
        choices=getattr(settings, 'PRIVACY_MODEL_CHOICES', None))

    class Meta:
        abstract = True


class DisplayName(models.Model):
    display_name = models.CharField(
        null=True,
        blank=True,
        **DISPLAY_NAME_ARGS
    )

    class Meta:
        abstract = True


class DisplayNameRequired(create_slug_mixin('display_name'), models.Model):
    display_name = models.CharField(
        **DISPLAY_NAME_ARGS
    )

    class Meta:
        abstract = True


class Description(models.Model):
    description = models.TextField(
        null=True,
        blank=True,
        **DESCRIPTION_ARGS
    )

    class Meta:
        abstract = True


class TopicTitleRequired(create_slug_mixin('title'), models.Model):
    title = models.CharField(
        **TITLE_ARGS
    )

    class Meta:
        abstract = True


def profile_picture_class_generator(upload_to, default=None):
    class ProfilePicture(models.Model):
        profile_picture = models.ImageField(
            null=True,
            blank=True,
            upload_to=upload_to,
            default=default
        )

        def save(self, **kwargs):
            return super().save(**kwargs)

        class Meta:
            abstract = True

    return ProfilePicture
