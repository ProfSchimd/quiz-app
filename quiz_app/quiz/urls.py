from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("start/", login_required(views.start), name="start"),
    path("<int:assignment_id>/create/", login_required(views.create), name="create"),
    path("<int:attempt_id>/quiz/", login_required(views.quiz), name="quiz")
]