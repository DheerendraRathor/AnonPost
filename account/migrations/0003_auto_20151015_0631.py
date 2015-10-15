# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20151015_0533'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='oauthtoken',
            name='user',
        ),
        migrations.DeleteModel(
            name='OAuthToken',
        ),
    ]
