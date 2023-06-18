from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("start/", login_required(views.start), name="start"),
    path("quiz/", login_required(views.quiz), name="quiz")
]