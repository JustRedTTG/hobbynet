# Generated by Django 4.2.3 on 2023-07-14 09:21

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_alter_profile_display_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, max_length=30, null=True, populate_from='pk', unique=True),
        ),
    ]