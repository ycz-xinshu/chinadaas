# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_auto_20141108_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='ping',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
