# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-07 13:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0006_auto_20170516_1638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textlabel',
            name='changed',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='translatedtext',
            name='changed',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='translatedtextlabel',
            name='changed',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]