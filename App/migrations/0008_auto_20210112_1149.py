# Generated by Django 2.2.12 on 2021-01-12 11:49

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0007_auto_20210111_2008'),
    ]

    operations = [
        migrations.AddField(
            model_name='step_parent',
            name='sender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='App.Employee'),
        ),
        migrations.AlterField(
            model_name='to_dolist',
            name='Publish_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 12, 11, 49, 39, 199249), verbose_name='发布时间'),
        ),
    ]
