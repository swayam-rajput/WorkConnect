# Generated by Django 4.2.2 on 2024-03-03 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newco', '0009_userprofile_profilepic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profilepic',
            field=models.ImageField(default='default.jpg', upload_to='profile_pics/'),
        ),
    ]
