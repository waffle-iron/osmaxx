# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-12 12:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversion', '0007_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parametrization',
            name='out_format',
            field=models.CharField(choices=[('fgdb', 'Esri File Geodatabase'), ('shapefile', 'Esri Shapefile'), ('gpkg', 'GeoPackage'), ('spatialite', 'SpatiaLite'), ('garmin', 'Garmin navigation & map data')], max_length=100, verbose_name='out format'),
        ),
    ]