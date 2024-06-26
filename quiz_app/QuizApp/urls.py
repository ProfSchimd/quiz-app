from django.contrib.auth.decorators import login_required, permission_required
from django.urls import path

from . import views

from .models import Collection
from django.views.generic.detail import DetailView

# TODO: Add login and permission restriction where appropriate
urlpatterns = [
    path("tag/new", login_required(views.CreateTagView.as_view()), name="tag_new"),
    path("subject/new",  login_required(views.CreateSubjectView.as_view()), name="subject_new"),
    
    path("question/show/<int:q_id>", views.question_show, name="question_show"),
    path("question/show", login_required(views.question_list), name="question_list"),
    path("question/export", views.question_export, name="question_export"),
    path("question/new",  views.question_create, name="question_new"),
    path("question/upload", views.question_upload, name="question_upload"),
    path("question/upload/confirm", views.question_upload_confirm, name="question_upload_confirm"),
    
    path("collection/from_questions", login_required(views.CreateCollectionView.as_view()), name="collection_from_questions"),
    
    path("collection/<int:pk>", DetailView.as_view(model=Collection, template_name="QuizApp/collection/collection_detail.html")),
    
    path("", views.index, name="index"),
    
    path("test", views.test_view, name="test_page")
   
]