# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-26 10:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0048_remove_old_choices_data'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='internshipchoice',
            unique_together=set([('student', 'internship', 'choice')]),
        ),
    ]
