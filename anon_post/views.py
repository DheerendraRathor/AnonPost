from django.conf import settings
from django.shortcuts import redirect
from stronghold.decorators import public
from django.shortcuts import render
from post.models import Site


@public
def index(request):
    if request.user.is_authenticated():
        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        return redirect(settings.LOGIN_URL)


def sites(request):
    all_sites = Site.objects.all()
    return render(request, 'anon_post/sites.html', {'sites': all_sites})


@public
def about(request):
    return render(request, 'anon_post/about.html', {})
