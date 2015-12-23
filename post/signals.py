from django.db.models import signals
from django.core.urlresolvers import reverse
import threading
from django.conf import settings
from anon_post.notification import send_mail
import urlparse
from models import Post, Reply
from oauth.request import UserSendMailAPIRequest


class SendMailToUserThread(threading.Thread):

    def __init__(self, subject, message, user):
        super(SendMailToUserThread, self).__init__()
        self.subject = subject
        self.message = message
        self.user = user

    def run(self):
        UserSendMailAPIRequest(self.subject, self.message, [], token=self.user.token).send()


def create_email_list(site, user):
    user_list = set(site.admins.all())
    user_list.add(user)
    return list(user_list)


def send_post_email(sender, instance, created, **kwargs):
    subject = "[Anon Post] %s" % instance.title
    message = """
    A new post has been added to Anon Post. Open in browser at %s

    Title: %s

    Message: %s
        """
    post_url = urlparse.urljoin(settings.BASE_URL, reverse('home:post', args=[instance.site.id, instance.id]))
    message = message % (post_url, instance.title, instance.message)
    user_list = create_email_list(instance.site, instance.user)
    for user in user_list:
        SendMailToUserThread(subject, message, user).start()


def send_reply_email(sender, instance, created, **kwargs):
    subject = "Re: [Anon Post] %s" % instance.post.title
    message = """
    A new reply has been added to Anon Post. Open post in browser at %s

    Message by %s: %s
    """
    poster = "Submitter" if instance.post.user == instance.user else "Admin"
    post_url = urlparse.urljoin(settings.BASE_URL, reverse('home:post', args=[instance.post.site.id, instance.post.id]))
    message = message % (post_url, poster, instance.message)
    user_list = create_email_list(instance.post.site, instance.user)
    for user in user_list:
        SendMailToUserThread(subject, message, user).start()


signals.post_save.connect(send_post_email, Post)
signals.post_save.connect(send_reply_email, Reply)


