# Generated by Django 4.2.3 on 2023-07-08 08:43

from django.db import migrations, models
import django_backblaze_b2.storage
import hobbynet.profiles.models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_profile_visibility'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default=None, null=True, upload_to=hobbynet.profiles.models.profile_image_generator),
        ),
    ]
