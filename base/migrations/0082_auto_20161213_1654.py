# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-13 15:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0081_auto_20161207_1432'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attribution',
            name='learning_unit',
        ),
        migrations.AlterField(
            model_name='attribution',
            name='learning_unit_year',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='learning_unit_year_attribution', to='base.LearningUnitYear'),
        ),
        migrations.AlterField(
            model_name='attribution',
            name='tutor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tutor_attribution', to='base.Tutor'),
        ),
    ]
