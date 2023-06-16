from datetime import datetime

from django.db import models
from django.conf import settings

class Quiz(models.Model):
    JSON = models.JSONField()
    description = models.TextField(max_length=512)
    active = models.BooleanField(default=True)
    subject = models.TextField(max_length=128)
    
class UserQuiz(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    result = models.JSONField(null=True)
    date = models.DateTimeField(null=True)
    