from django.contrib.auth.decorators import login_required, permission_required
from django.urls import path

from . import views

urlpatterns = [
    path("tag/new", login_required(views.CreateTagView.as_view())),
    path("subject/new",  views.CreateSubjectView.as_view()),
    
    path("question/new",  views.create_question),
    path("question/all", views.question_list),
    path("question/upload", views.question_upload, name="question_upload"),
    path("question/upload/confirm", views.question_upload_confirm, name="question_upload_confirm"),
    
    path("", views.index, name="index"),
   
]