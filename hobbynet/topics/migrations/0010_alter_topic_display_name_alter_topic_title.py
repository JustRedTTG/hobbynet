# Generated by Django 4.2.3 on 2023-07-14 08:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0009_alter_topic_display_name_alter_topic_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='display_name',
            field=models.CharField(blank=True, max_length=60, null=True, validators=[django.core.validators.MinLengthValidator(5)]),
        ),
        migrations.AlterField(
            model_name='topic',
            name='title',
            field=models.CharField(max_length=85, validators=[django.core.validators.MinLengthValidator(5)]),
        ),
    ]
