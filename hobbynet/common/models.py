import random
from django.core.files.base import ContentFile
from django.core.validators import MinLengthValidator
from django.db import models
from django.conf import settings
from django import forms
from django_backblaze_b2 import BackblazeB2Storage
import py_avataaars as pa

# Create your models here.

DISPLAY_NAME_ARGS = {
    'max_length': 30,
    'validators': [MinLengthValidator(6)]
}

TITLE_ARGS = {
    'max_length': 30,
    'validators': [MinLengthValidator(8)]
}


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


class DisplayNameRequired(models.Model):
    display_name = models.CharField(
        **DISPLAY_NAME_ARGS
    )

    class Meta:
        abstract = True


class DisplayNameForm(forms.Form):
    display_name = forms.CharField(
        required=False,
        **DISPLAY_NAME_ARGS
    )

    class Meta:
        abstract = True


class DisplayNameFormRequired(forms.Form):
    display_name = forms.CharField(
        required=True,
        **DISPLAY_NAME_ARGS
    )

    class Meta:
        abstract = True


class TopicTitleRequired(models.Model):
    title = models.CharField(
        **TITLE_ARGS
    )

    class Meta:
        abstract = True

class TopicTitleFormRequired(forms.Form):
    title = forms.CharField(
        required=True,
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
