# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-14 18:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20160504_0309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chessuser',
            name='username',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
