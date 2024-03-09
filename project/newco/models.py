from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    phno = models.IntegerField()
    gender = models.CharField(max_length=8)
    is_verified = models.BooleanField(default=False)
    aadhar = models.CharField(max_length=12,default="")
    profilepic = models.ImageField(default='default.jpg',unique=False,upload_to='profile_pics/')
    aadharpdf = models.FileField(upload_to="ssn/",null=True,blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    pdfpsd = models.CharField(max_length=8,default="")
    
    def __str__(self):
        return f'{self.user}'

class Job(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    job_specification = models.CharField(default=None,max_length=255)
    salary = models.CharField(max_length=32)
    location = models.CharField(max_length=32)
    people_applied = models.IntegerField(default=0)
    applied = models.ManyToManyField(User,related_name='users_applied',blank=True)

    def __str__(self):
        return f'{self.title}'