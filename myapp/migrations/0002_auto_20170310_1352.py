# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('app_id', models.IntegerField(serialize=False, primary_key=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('time_of_arrival', models.DateTimeField()),
                ('start_time', models.DateTimeField(null=True)),
                ('wait_time', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('doctor_id', models.IntegerField()),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('total_wait_time', models.IntegerField(null=True)),
                ('total_patients', models.IntegerField(null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Patient',
        ),
    ]
