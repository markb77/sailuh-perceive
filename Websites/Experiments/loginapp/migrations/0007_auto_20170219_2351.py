# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-19 23:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loginapp', '0006_auto_20170219_1944'),
    ]

    operations = [
        migrations.RenameField(
            model_name='click_log',
            old_name='click_acton',
            new_name='click_action',
        ),
    ]
