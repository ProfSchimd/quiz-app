from django.db import models
from django.conf import settings

class Assignment(models.Model):
    description = models.TextField(max_length=250)
    active = models.BooleanField()
    def __str__(self):
        return f"{self.description}"
    

class Quiz(models.Model):
    JSON = models.JSONField()
    description = models.TextField(max_length=512)
    subject = models.TextField(max_length=128)
    def __str__(self):
        return f"{self.description}"

class Attempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True, blank=True)
    answer = models.JSONField(null=True, blank=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.user} attempt on {self.assignment} (started {self.start})"
    
    