# Generated by Django 4.2.2 on 2024-03-03 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newco', '0008_userprofile_is_verified_alter_job_job_specification'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='profilepic',
            field=models.ImageField(default='default.jpg', upload_to='profile_pics'),
        ),
    ]
