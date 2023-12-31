# Generated by Django 4.2.3 on 2023-07-14 09:28

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0013_alter_post_slug_alter_post_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, max_length=30, null=True, populate_from='title', unique=False),
        ),
    ]
