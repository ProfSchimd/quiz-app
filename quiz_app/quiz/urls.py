from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:assignment_id>/start/", login_required(views.start), name="start"),
    path("<int:assignment_id>/create/", login_required(views.create), name="create"),
    path("<int:attempt_id>/save/", login_required(views.save), name="save"),
    path("<int:attempt_id>/quiz/", login_required(views.quiz), name="quiz"),
    path("<int:attempt_id>/delete/", login_required(views.delete), name="delete")
]