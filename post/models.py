from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
from django.utils.encoding import python_2_unicode_compatible
from redactor.fields import RedactorField


@python_2_unicode_compatible
class Site(models.Model):
    creator = models.ForeignKey(User, related_name='created_sites')
    admins = models.ManyToManyField(User, related_name='administrated_sites', blank=True)
    name = models.CharField(max_length=256)
    description = RedactorField(verbose_name='Description for this site')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_demo = models.BooleanField(default=False)
    _history_ = HistoricalRecords()

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(User)
    site = models.ForeignKey(Site)
    title = models.CharField(max_length=255)
    message = RedactorField(help_text='Details of your post')
    created = models.DateTimeField(auto_now_add=True)


class Reply(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post, related_name='replies')
    message = RedactorField()
    created = models.DateTimeField(auto_now_add=True)
