# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-31 01:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chess_logic', '0008_auto_20160505_0103'),
    ]

    operations = [
        migrations.AddField(
            model_name='chessgame',
            name='looking_for_move',
            field=models.BooleanField(default=False),
        ),
    ]
