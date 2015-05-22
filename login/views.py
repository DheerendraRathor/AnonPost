from django.shortcuts import render, redirect
from forms import LoginForm
from stronghold.decorators import public
import django.contrib.auth as auth
from django.contrib.auth import authenticate
from django.conf import settings

# Create your views here.

@public
def login(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        remember = form.cleaned_data['remember']

        if remember:
            # Yearlong Session
            request.session.set_expiry(24*265*3600)
        else:
            request.session.set_expiry(0)

        user = authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            form.add_error(None, "Unable to authorize user. Try again!")
    return render(request, 'login.html', {'form': form})


@public
def logout(request):
    user = request.user
    auth.logout(request, user)
    redirect(settings.LOGIN_URL)