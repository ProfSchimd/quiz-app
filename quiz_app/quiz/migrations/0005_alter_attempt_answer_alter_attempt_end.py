# Generated by Django 4.2.2 on 2023-07-15 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_assignment_attempt_remove_quiz_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attempt',
            name='answer',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='attempt',
            name='end',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
