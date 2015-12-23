from django.conf import settings


def admin_usernames(request):
    return {'ADMIN_USERNAMES' : settings.ADMIN_USERNAMES}