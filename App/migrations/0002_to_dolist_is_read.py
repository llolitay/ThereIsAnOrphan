# Generated by Django 2.2.12 on 2021-01-09 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='to_dolist',
            name='Is_read',
            field=models.BooleanField(default=False, verbose_name='是否已阅'),
        ),
    ]
