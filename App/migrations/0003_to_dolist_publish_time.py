# Generated by Django 2.2.12 on 2021-01-10 21:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_to_dolist_is_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='to_dolist',
            name='Publish_time',
            field=models.DateField(default=datetime.datetime(2021, 1, 10, 21, 14, 37, 311642), verbose_name='发布时间'),
        ),
    ]
