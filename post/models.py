from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


class Reply(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post, related_name='replies')
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

