# Generated by Django 4.2.3 on 2023-07-08 07:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_post_date_created_alter_post_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='privacy',
            new_name='visibility',
        ),
    ]
