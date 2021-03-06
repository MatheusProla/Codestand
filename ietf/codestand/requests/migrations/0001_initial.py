# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CodeRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mentor', models.IntegerField(null=True, blank=True)),
                ('estimated_lof', models.FloatField(null=True, blank=True)),
                ('additional_information', models.TextField(null=True, blank=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
