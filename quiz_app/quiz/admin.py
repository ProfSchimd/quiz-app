from django.contrib import admin

from .models import Quiz, Assignment, Attempt

admin.site.register(Quiz)
admin.site.register(Assignment)
admin.site.register(Attempt)
