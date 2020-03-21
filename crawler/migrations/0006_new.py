# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2020-03-18 07:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0005_auto_20200312_0139'),
    ]

    operations = [
        migrations.CreateModel(
            name='New',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idCrawlerJob', models.CharField(max_length=100, null=True)),
                ('type', models.TextField(null=True)),
                ('link', models.TextField(null=True)),
                ('imageLink', models.TextField(null=True)),
                ('title', models.TextField(null=True)),
                ('description', models.TextField(null=True)),
            ],
        ),
    ]