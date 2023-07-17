# Generated by Django 4.2.3 on 2023-07-14 09:44
from urllib.parse import quote

from django.db import migrations
import django_extensions.db.fields


def set_slug_field(apps, schema_editor):
    Profile = apps.get_model('profiles', 'Profile')
    for profile in Profile.objects.all():
        profile.slug = quote(profile.display_name.replace(' ', '-'))[:30]
        profile.save()

class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_alter_profile_slug'),
    ]

    operations = [
        migrations.RunPython(set_slug_field),
        migrations.AlterField(
            model_name='profile',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, max_length=30, populate_from='display_name', unique=False),
            preserve_default=False,
        ),
    ]