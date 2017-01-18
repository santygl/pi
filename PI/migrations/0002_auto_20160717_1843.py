# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PI', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kiply',
            name='kiply_key',
            field=models.CharField(default=None, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='twitter',
            name='key',
            field=models.CharField(default=None, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='twitter',
            name='secret',
            field=models.CharField(default=None, max_length=254, null=True),
        ),
    ]
