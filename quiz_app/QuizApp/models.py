from datetime import datetime
from django.contrib.auth.models import User
from django.db import models

# This is a model to extend default Django user
# See documentation https://docs.djangoproject.com/en/4.2/topics/auth/customizing/
class UserProfile(models.Model):
    USER_TYPE = [
        ("TEA", "Teacher"),
        ("STU", "Student")
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(max_length=256)
    type = models.CharField(max_length=3, choices=USER_TYPE)
    

class Group(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    CLASS_LEVEL =[
        (1, 'Prima'),
        (2, 'Seconda'),
        (3, 'Terza'),
        (4, 'Quarta'),
        (5, 'Quinta'),
    ]
    level = models.IntegerField(choices=CLASS_LEVEL, null=True)
    section = models.CharField(max_length=8, null=True)
    year = models.CharField(max_length=16, null=True)
    members = models.ManyToManyField(User)
    
    

class Subject(models.Model):
    name = models.CharField(max_length=128, unique=True)
    short_name = models.CharField(max_length=8)
    description = models.TextField(null=True)
    
    def __str__(self) -> str:
        return f"{self.name} ({self.short_name})"
    

class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True)
    description = models.TextField(null=True)
    
    def __str__(self) -> str:
        return f"{self.name}"

class Question(models.Model):
    QUESTION_TYPE = [
        ("SINGLE", "Single"),
        ("MULTIPLE", "Multiple"),
        ("INVERTIBLE", "Invertible"),
        ("FILL", "Fill"),
    ]
    question_type = models.CharField(max_length=16, choices=QUESTION_TYPE)
    # ToDo: set check on range
    weight = models.IntegerField(default=1)
    text_and_keys = models.JSONField()
    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    subject = models.ForeignKey(Subject, null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)
    
    def __str__(self):
        
        return f"{self.id}: {self.text_and_keys} ({self.get_question_type_display()})"
    
    

class Collection(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    topic = models.CharField(max_length=64, null=True, blank=True)
    subject = models.ForeignKey(Subject, null=True, blank=True, on_delete=models.SET_NULL)
    is_virtual = models.BooleanField(default=False)
    questions = models.ManyToManyField(Question)
    
class Assignment(models.Model):
    # General description
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    # Generation options
    question_number = models.IntegerField()
    generating_options = models.JSONField(null=True, blank=True)
    # Attempt options
    deadline = models.DateTimeField(blank=True, null=True)
    timer = models.DurationField(blank=True, null=True)
    max_attempts = models.IntegerField(default=1)
    is_resumable = models.BooleanField(default=True)
    is_deletable = models.BooleanField(default=False)
    score = models.IntegerField(null=True, blank=True, default=10)
    # Feedback options
    FB_TYPE = [
        ("TEAC", "Teacher review"),
        ("PEER", "Peer review")
    ]
    feedback_type = models.CharField(max_length=4, choices=FB_TYPE, default="TEAC")
    feedback_delay = models.DurationField(blank=True, null=True)
    FB_REVIEWER = [
        (0, 'Teacher assigned'),
        (1, 'Random assigned')
    ]
    feedback_reviewer = models.IntegerField(choices=FB_REVIEWER, default=0)
    FB_BLIND = [
        (0, 'Open'),
        (1, 'Hide Reviewer'),
        (2, 'Hide Author'),
        (3, 'Double Blind')
    ]
    feedback_blind = models.IntegerField(choices=FB_BLIND, default=0)
    # Foreign keys
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    
class Attempt(models.Model):
    start = models.DateTimeField(null=True, blank=True)
    seed = models.CharField(max_length=32, blank=True, default="")
    json_text = models.JSONField(null=True, blank=True)
    saved_answer = models.JSONField(null=True, blank=True)
    saved_time = models.DateTimeField(null=True, blank=True)
    submit_answer = models.JSONField(null=True, blank=True)
    submit_time = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attempting_user")
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, null=True)

class Feedback(models.Model):
    review = models.JSONField(null=True)
    summary = models.TextField(null=True)
    submission_date = models.DateTimeField(null=True)
    read_date = models.DateTimeField(null=True)
    rebuttal = models.JSONField(null=True)
    is_archived = models.BooleanField(default=False)
    attempt = models.OneToOneField(Attempt, null=True, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    
class Notification(models.Model):
    NOTIFICATION_EVENTS = [
        (0, "New assignment"),
        (1, "New review requested"),
        (2, "New feedback received")
    ]
    event = models.IntegerField(default=0, choices=NOTIFICATION_EVENTS)
    text = models.TextField(default="")
    sent_date = models.DateTimeField(default=datetime.now, blank=True)
    read_date = models.DateTimeField(null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    
class TeacherClass(models.Model):
    teacher = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    class_group = models.ForeignKey(Group, null=True, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, null=True, on_delete=models.CASCADE)