# Generated by Django 4.2.3 on 2023-07-14 09:44
from urllib.parse import quote

from django.db import migrations
import django_extensions.db.fields


def set_slug_field(apps, schema_editor):
    Topic = apps.get_model('topics', 'Topic')
    for topic in Topic.objects.all():
        topic.slug = quote(topic.title.replace(' ', '-'))[:30]
        topic.save()

class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0012_alter_topic_slug'),
    ]

    operations = [
        migrations.RunPython(set_slug_field),
        migrations.AlterField(
            model_name='topic',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, max_length=30, populate_from='title', unique=False),
            preserve_default=False,
        ),
    ]
