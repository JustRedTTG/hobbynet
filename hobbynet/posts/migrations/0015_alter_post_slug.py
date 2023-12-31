# Generated by Django 4.2.3 on 2023-07-14 09:44
from urllib.parse import quote

from django.db import migrations
import django_extensions.db.fields

def set_slug_field(apps, schema_editor):
    Post = apps.get_model('posts', 'Post')
    for post in Post.objects.all():
        post.slug = quote(post.title.replace(' ', '-'))[:30]
        post.save()


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0014_alter_post_slug'),
    ]

    operations = [
        migrations.RunPython(set_slug_field),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, max_length=30, populate_from='title', unique=False),
            preserve_default=False,
        ),
    ]
