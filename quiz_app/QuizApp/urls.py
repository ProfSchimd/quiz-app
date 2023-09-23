from django.contrib.auth.decorators import login_required, permission_required
from django.urls import path

from . import views

urlpatterns = [
    path("tag/new", login_required(views.CreateTagView.as_view())),
    path("subject/new",  views.CreateSubjectView.as_view()),
    path("question/new",  views.create_question),
    
    path("", views.index, name="index"),
   
]