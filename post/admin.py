from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Site


@admin.register(Site)
class SiteAdmin(SimpleHistoryAdmin):
    list_display = ['id', 'name', 'creator', 'created', 'is_demo']

