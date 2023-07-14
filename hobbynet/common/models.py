from django_extensions.db.fields import AutoSlugField
from django.core.validators import MinLengthValidator
from django_backblaze_b2 import BackblazeB2Storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.db import models
import py_avataaars as pa
import unicodedata
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

def slugify(value):
    return unicodedata.normalize('NFKC', value).lower().replace(' ', '-')

def create_slug_mixin(slug_field):
    class SlugMixin(models.Model):
        slug = AutoSlugField(
            populate_from=slug_field,
            slugify_function=slugify,
            max_length=SLUG_MAX_LENGTH,
            unique=True,
            null=True,
            blank=True
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


class TopicTitleRequired(create_slug_mixin('title'), models.Model):
    title = models.CharField(
        **TITLE_ARGS
    )

    class Meta:
        abstract = True


def profile_picture_class_generator(upload_to, default=None, blank: bool = False):
    class ProfilePicture(models.Model):
        profile_picture = models.ImageField(
            null=True,
            blank=True,
            storage=BackblazeB2Storage,
            upload_to=upload_to,
            default=default
        )

        def save(self, **kwargs):
            if blank:
                return super().save(**kwargs)
            if not self.profile_picture:
                avataaar = pa.PyAvataaar(
                    style=random.choice(list(pa.AvatarStyle)),
                    skin_color=random.choice(list(pa.SkinColor)),
                    hair_color=random.choice(list(pa.HairColor)),
                    top_type=random.choice(list(pa.TopType)),
                    facial_hair_type=random.choice(list(pa.FacialHairType)),
                    clothe_type=random.choice(list(pa.ClotheType)),
                    mouth_type=random.choice(list(pa.MouthType)),
                    eye_type=random.choice(list(pa.EyesType)),
                    eyebrow_type=random.choice(list(pa.EyebrowType)),
                    accessories_type=random.choice(list(pa.AccessoriesType)),
                    background_color=random.choice(list(pa.Color)),
                )
                file = avataaar.render_png()
                self.profile_picture.save('avataaar.png', ContentFile(file), save=False)

            return super().save(**kwargs)

        class Meta:
            abstract = True

    return ProfilePicture
