# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-12-19 07:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gathering',
            name='users',
            field=models.ManyToManyField(related_name='gathers', to=settings.AUTH_USER_MODEL, verbose_name='参加者'),
        ),
    ]
