__author__ = 'dheerendra'

from django.conf import settings
from django.shortcuts import redirect
from stronghold.decorators import public

@public
def index(request):
    if request.user.is_authenticated():
        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        return redirect(settings.LOGIN_URL)
