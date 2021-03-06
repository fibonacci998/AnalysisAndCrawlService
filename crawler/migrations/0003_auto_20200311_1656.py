# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2020-03-11 16:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0002_realestateobject_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realestateobject',
            name='address',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='realestateobject',
            name='area',
            field=models.DecimalField(decimal_places=5, max_digits=19, null=True),
        ),
        migrations.AlterField(
            model_name='realestateobject',
            name='balconyDirection',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='realestateobject',
            name='codePost',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='realestateobject',
            name='email',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='realestateobject',
            name='homeDirection',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='realestateobject',
            name='idCrawlerJob',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='realestateobject',
            name='interior',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='realestateobject',
            name='latitude',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='realestateobject',
            name='link',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='realestateobject',
            name='longitude',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='realestateobject',
            name='mobile',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='realestateobject',
            name='nameOwner',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='realestateobject',
            name='numberBedrooms',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='realestateobject',
            name='numberFloor',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='realestateobject',
            name='numberToilets',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='realestateobject',
            name='price',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='realestateobject',
            name='projectName',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='realestateobject',
            name='projectOwner',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='realestateobject',
            name='projectSize',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='realestateobject',
            name='sizeFront',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='realestateobject',
            name='title',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='realestateobject',
            name='type',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='realestateobject',
            name='typePost',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='realestateobject',
            name='wardin',
            field=models.BigIntegerField(null=True),
        ),
    ]
