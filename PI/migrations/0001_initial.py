# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Kiply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kiply_key', models.CharField(default=None, max_length=254)),
                ('user', models.OneToOneField(related_name='kiply', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Twitter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('secret', models.CharField(default=None, max_length=254)),
                ('key', models.CharField(default=None, max_length=254)),
                ('user', models.OneToOneField(related_name='twitter', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
