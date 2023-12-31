# Generated by Django 4.2.2 on 2023-06-18 09:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0003_alter_userquiz_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=250)),
                ('active', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Attempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(null=True)),
                ('end', models.DateTimeField(null=True)),
                ('answer', models.JSONField(null=True)),
                ('active', models.BooleanField(default=True)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.assignment')),
            ],
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='active',
        ),
        migrations.DeleteModel(
            name='UserQuiz',
        ),
        migrations.AddField(
            model_name='attempt',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.quiz'),
        ),
        migrations.AddField(
            model_name='attempt',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
