from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100,null=True,blank=True)
    username = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(max_length=100,null=True,blank=True)
    profile_pic = models.ImageField(upload_to='avatar',default='dennis.jpg',blank=True,null=True)
    bio = models.TextField()
    facebook_id = models.URLField(blank=True,null=True)
    twitter_id = models.URLField(blank=True,null=True)
    linkedin_id = models.URLField(blank=True,null=True)

    def __str__(self):
        return self.user.username


