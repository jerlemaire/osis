# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-13 10:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0096_auto_20170120_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='learningunitcomponent',
            name='coefficient_repetition',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
