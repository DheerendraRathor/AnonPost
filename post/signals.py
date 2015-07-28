__author__ = 'dheerendra'

from django.db.models import signals
from django.core.urlresolvers import reverse
import threading
from django.conf import settings
from anon_post.notification import send_mail
import urlparse
from models import Post, Reply


def create_email_list(user_email):
    email_list = settings.ADMIN_USERNAMES
    email_list = [admin + "@iitb.ac.in" for admin in email_list]
    email_list.append(user_email)
    return list(set(email_list))


class EmailThread(threading.Thread):

    def __init__(self, subject, message, email_list):
        super(EmailThread, self).__init__()
        self.subject = subject
        self.message = message
        self.email_list = email_list

    def run(self):
        send_mail(self.subject, self.message, self.email_list)


def send_post_email(sender, instance, created, **kwargs):
    subject = "[Anon Post] %s" % instance.title
    message = """
    A new post has been added to Anon Post. Open in browser at %s

    Title: %s

    Message: %s
        """
    post_url = urlparse.urljoin(settings.BASE_URL, reverse('home:post', args=[instance.id]))
    message = message % (post_url, instance.title, instance.message)
    email_list = create_email_list(instance.user.email)
    email_thread = EmailThread(subject, message, email_list)
    email_thread.start()


def send_reply_email(sender, instance, created, **kwargs):
    subject = "Re: [Anon Post] %s" % instance.post.title
    message = """
    A new reply has been added to Anon Post. Open post in browser at %s

    Message by %s: %s
    """
    poster = "Submitter" if instance.post.user == instance.user else "Admin"
    post_url = urlparse.urljoin(settings.BASE_URL, reverse('home:post', args=[instance.post.id]))
    message = message % (post_url, poster, instance.message)
    email_list = create_email_list(instance.post.user.email)
    email_thread = EmailThread(subject, message, email_list)
    email_thread.start()


signals.post_save.connect(send_post_email, Post)
signals.post_save.connect(send_reply_email, Reply)


