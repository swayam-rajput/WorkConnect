# Generated by Django 4.2.2 on 2024-04-18 14:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newco', '0014_alter_userprofile_aadharpdf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='aadharpdf',
            field=models.FileField(default='null', null=True, upload_to='ssn/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])]),
        ),
    ]