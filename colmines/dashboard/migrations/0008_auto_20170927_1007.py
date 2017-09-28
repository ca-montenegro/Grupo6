# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-27 15:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_auto_20170927_1005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alerta',
            name='idUbicacion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.Ubicacion'),
        ),
        migrations.AlterField(
            model_name='alerta',
            name='time',
            field=models.TimeField(null=True, verbose_name='time'),
        ),
        migrations.AlterField(
            model_name='alerta',
            name='tipoAlerta',
            field=models.CharField(max_length=128, null=True, verbose_name='tipoAlerta'),
        ),
    ]