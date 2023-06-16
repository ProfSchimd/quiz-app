from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("choose/", login_required(views.choose), name="choose"),
    path("quiz/", login_required(views.quiz), name="quiz")
]