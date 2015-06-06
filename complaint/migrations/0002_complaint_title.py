# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('complaint', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='title',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]