# Generated by Django 4.2.3 on 2023-07-14 08:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_alter_profile_display_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='display_name',
            field=models.CharField(max_length=60, validators=[django.core.validators.MinLengthValidator(5)]),
        ),
    ]
