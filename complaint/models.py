from django.db import models

# Create your models here.

class Complaint(models.Model):
	message = models.TextField()