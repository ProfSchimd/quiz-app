# Generated by Django 4.2.4 on 2023-09-21 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuizApp', '0005_alter_subject_name_alter_tag_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='attempt',
            name='json_text',
            field=models.JSONField(null=True),
        ),
    ]
