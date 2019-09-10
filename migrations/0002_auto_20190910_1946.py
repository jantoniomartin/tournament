# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2019-09-10 19:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='description_en',
            field=models.TextField(default='', verbose_name='description'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tournament',
            name='prize_en',
            field=models.TextField(default='', verbose_name='prize'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tournament',
            name='rules_en',
            field=models.URLField(default='', verbose_name='rules'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tournament',
            name='title_en',
            field=models.CharField(default='', max_length=100, verbose_name='title'),
            preserve_default=False,
        ),
    ]