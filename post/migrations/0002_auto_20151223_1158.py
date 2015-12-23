# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalsite',
            old_name='short_description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='site',
            old_name='short_description',
            new_name='description',
        ),
    ]
