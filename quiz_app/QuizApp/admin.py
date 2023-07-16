from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Assignment, Attempt, Collection, Group, Feedback, Notification, Question, Subject, Tag, TeacherClass, UserProfile

# Register your models here.
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    
class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]


admin.site.register(Assignment)
admin.site.register(Attempt)
admin.site.register(Collection)
admin.site.register(Group)
admin.site.register(Feedback)
admin.site.register(Notification)
admin.site.register(Question)
admin.site.register(Subject)
admin.site.register(Tag)
admin.site.register(TeacherClass)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
