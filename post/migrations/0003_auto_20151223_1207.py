# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_auto_20151223_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalsite',
            name='description',
            field=models.TextField(help_text=b'Description for this site'),
        ),
        migrations.AlterField(
            model_name='site',
            name='description',
            field=models.TextField(help_text=b'Description for this site'),
        ),
    ]
