# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('patient_id', models.IntegerField(unique=True, max_length=100, blank=True)),
                ('name', models.CharField(max_length=256)),
                ('date_of_birth', models.DateField(null=True)),
                ('email', models.CharField(max_length=256, blank=True)),
                ('message_status', models.CharField(max_length=256, blank=True)),
                ('year', models.IntegerField(max_length=100, blank=True)),
            ],
        ),
    ]
