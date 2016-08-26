# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-27 18:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppDeployLogModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=50)),
                ('time', models.DateTimeField()),
                ('target', models.CharField(max_length=100)),
                ('application', models.CharField(max_length=100)),
                ('mapping', models.CharField(max_length=20)),
                ('success_hosts', models.CharField(max_length=500)),
                ('failed_hosts', models.CharField(max_length=500)),
                ('total', models.IntegerField()),
                ('log', models.TextField()),
                ('duration', models.CharField(max_length=500)),
            ],
            options={
                'db_table': 'ops_app_deploy_log',
            },
        ),
        migrations.CreateModel(
            name='CmdRunLogModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=30)),
                ('time', models.DateTimeField()),
                ('target', models.CharField(max_length=100)),
                ('mapping', models.CharField(max_length=50)),
                ('cmd', models.CharField(max_length=500)),
                ('hosts', models.CharField(max_length=500)),
                ('total', models.IntegerField()),
            ],
            options={
                'db_table': 'ops_cmd_run_log',
            },
        ),
        migrations.CreateModel(
            name='HostInfoModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=100)),
                ('ipaddress', models.CharField(max_length=200)),
                ('cpuinfo', models.CharField(max_length=50)),
                ('meminfo', models.CharField(max_length=50)),
                ('group', models.CharField(max_length=50)),
                ('osinfo', models.CharField(max_length=20)),
                ('area', models.CharField(max_length=100)),
                ('usage', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'ops_host_info',
            },
        ),
    ]
