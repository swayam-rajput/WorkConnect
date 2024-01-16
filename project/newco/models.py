from django.db import models
from django.contrib.auth.models import User
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    phno = models.IntegerField()
    gender = models.CharField(max_length=8)
    
    def __str__(self):
        return f'{self.user}'

class Job(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    job_specification = models.CharField(max_length=255)
    salary = models.CharField(max_length=32)
    location = models.CharField(max_length=32)
    people_applied = models.IntegerField(default=0)
    applied = models.ManyToManyField(User,related_name='users_applied',blank=True)

    def __str__(self):
        return f'{self.title}'