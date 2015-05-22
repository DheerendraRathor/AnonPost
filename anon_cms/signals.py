__author__ = 'dheerenr'

from django.dispatch import receiver
from django_auth_ldap.backend import ldap_error
import logging

logger = logging.getLogger(__name__)

@receiver(ldap_error)
def handle_ldap_error_signal(sender, **kwargs):
    context = kwargs.get("context")
    exception = kwargs.get("exception")
    logger.info("LDAP Error occurred %s, %s", context, str(exception))