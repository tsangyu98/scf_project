# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-12-19 07:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recruit',
            name='users',
            field=models.ManyToManyField(related_name='retruits', to=settings.AUTH_USER_MODEL, verbose_name='收藏者'),
        ),
        migrations.AddField(
            model_name='enterprise',
            name='users',
            field=models.ManyToManyField(related_name='enterpises', to=settings.AUTH_USER_MODEL, verbose_name='收藏者'),
        ),
    ]
