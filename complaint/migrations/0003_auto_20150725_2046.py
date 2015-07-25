# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('complaint', '0002_complaint_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reply',
            name='complaint',
            field=models.ForeignKey(related_name='replies', to='complaint.Complaint'),
        ),
    ]
