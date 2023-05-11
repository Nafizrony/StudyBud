from django.db import models
from django.contrib.auth.models import User
from devaccounts.models import Profile
import uuid

# Create your models here.

class Topics(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name
    

class Room(models.Model):
    host = models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True)
    topic = models.ForeignKey(Topics,on_delete=models.SET_NULL,null=True)
    title = models.CharField(max_length=288)
    description = models.TextField()
    participants = models.ManyToManyField(Profile,related_name='participants',blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title
    
class Messages(models.Model):
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.body


