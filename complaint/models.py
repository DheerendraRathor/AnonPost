from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Complaint(models.Model):
    user = models.ForeignKey(User)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


class Reply(models.Model):
    user = models.ForeignKey(User)
    complaint = models.ForeignKey(Complaint)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

