from django.db import models

from QuizApp.models import Subject

class QuizFile(models.Model):
    path = models.CharField(max_length=512, unique=True, blank=False,
                            name=False)
    subject = models.ForeignKey(Subject, default=None, blank=True,
                                null=True, on_delete=models.SET_NULL)
    
    def name(self):
        return self.path.rpartition("/")[0].rpartition(".")[0]
    
    def __str__(self):
        return f"{self.name()} ({self.path})"
