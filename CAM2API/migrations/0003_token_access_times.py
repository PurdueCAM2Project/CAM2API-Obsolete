# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-14 17:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CAM2API', '0002_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='access_times',
            field=models.PositiveIntegerField(default=0, verbose_name='Access_times'),
        ),
    ]