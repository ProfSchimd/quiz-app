from django.db import models

# This is a model to extend default Django user
# See documentation https://docs.djangoproject.com/en/4.2/topics/auth/customizing/
class UserProfile(models.Model):
    USER_TYPE = [
        ("TEA", "Teacher"),
        ("STU", "Student")
    ]
    website = models.URLField(max_length=255)
    type = models.CharField(max_length=3, choices=USER_TYPE)
