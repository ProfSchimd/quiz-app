# Generated by Django 4.2.2 on 2023-06-14 19:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userquiz',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='userquiz',
            name='result',
            field=models.JSONField(null=True),
        ),
    ]
