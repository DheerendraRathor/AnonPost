# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OAuthToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_created=True)),
                ('refresh_token', models.CharField(max_length=255)),
                ('access_token', models.CharField(max_length=255)),
                ('token_type', models.CharField(max_length=16)),
                ('scope', models.TextField()),
                ('expires_in', models.IntegerField()),
                ('user', models.OneToOneField(related_name='token', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
