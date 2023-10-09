from django.contrib.auth.decorators import login_required, permission_required
from django.urls import path

from . import views

# TODO: Add login and permission restriction where appropriate
urlpatterns = [
    path("tag/new", login_required(views.CreateTagView.as_view()), name="tag_new"),
    path("subject/new",  login_required(views.CreateSubjectView.as_view()), name="subject_new"),
    
    path("question/show/<int:q_id>", views.question_show, name="question_show"),
    path("question/show/all", views.question_list, name="question_show_all"),
    path("question/new",  views.create_question, name="question_new"),
    path("question/upload", views.question_upload, name="question_upload"),
    path("question/upload/confirm", views.question_upload_confirm, name="question_upload_confirm"),
    
    path("", views.index, name="index"),
   
]