from django.db import models
from django.contrib.auth.models import User
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    phno = models.IntegerField()
    gender = models.CharField(max_length=8)
    
    def __str__(self):
        return f'{self.user}'
    