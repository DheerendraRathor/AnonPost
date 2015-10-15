from django.shortcuts import render, redirect
from stronghold.decorators import public
import django.contrib.auth as auth
from django.contrib.auth.models import User
from django.conf import settings
from django.views.decorators.http import require_safe
from oauth.authorization import Authorization
from oauth.exceptions import OAuthError
from oauth.models import OAuthToken


@public
@require_safe
def authorize(request):
    if request.user.is_authenticated():
        if request.GET.get('next') != '' and request.GET.get('next') is not None:
            return redirect(request.GET.get('next'))
        else:
            return redirect(settings.LOGIN_REDIRECT_URL)
    try:
        token = Authorization(request).get_token()
    except OAuthError as e:
        return render(request, 'login.html', {'error': e.message})

    user, created = User.objects.get_or_create(username=token.refresh_token)
    try:
        oauth_token = user.token
    except OAuthToken.DoesNotExist:
        oauth_token = None
    if not oauth_token:
        user.set_unusable_password()
        oauth_token = OAuthToken(
            user=user,
            refresh_token=token.refresh_token,
            access_token=token.access_token,
            expires_in=token.expires_in,
            token_type=token.token_type,
            scope=token.scope
        )
    else:
        oauth_token.refresh_token = token.refresh_token
        oauth_token.access_token = token.access_token
        oauth_token.expires_in = token.expires_in
        oauth_token.token_type = token.token_type
        oauth_token.scope = token.scope
    oauth_token.save()
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    auth.login(request, user)
    if request.GET.get('state') != '' and request.GET.get('state') is not None:
        return redirect(request.GET.get('state'))
    else:
        return redirect(settings.LOGIN_REDIRECT_URL)


@public
def logout(request):
    auth.logout(request)
    return redirect(settings.LOGIN_URL)
