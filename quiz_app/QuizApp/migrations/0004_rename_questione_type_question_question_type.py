# Generated by Django 4.2.4 on 2023-09-19 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('QuizApp', '0003_teacherclass'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='questione_type',
            new_name='question_type',
        ),
    ]
