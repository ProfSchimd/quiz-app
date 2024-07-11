from django.contrib.auth.decorators import login_required, permission_required
from django.urls import path

from . import views

from .models import Collection
from django.views.generic.detail import DetailView

# TODO: Add login and permission restriction where appropriate
urlpatterns = [
    path("tag/add", login_required(views.CreateTagView.as_view()), name="tag_add"),
    #path("tag/all", login_required(views.tag_all), name="tag_all"),
    path("subject/add",  login_required(views.CreateSubjectView.as_view()), name="subject_add"),
    path("subject/all", login_required(views.subject_all), name="subject_all"),
    
    path("question/show/<int:q_id>", views.question_show, name="question_show"),
    path("question/list", login_required(views.question_list), name="question_list"),
    path("question/export", views.question_export, name="question_export"),
    path("question/add",  views.question_create, name="question_add"),
    path("question/upload", views.question_upload, name="question_upload"),
    path("question/upload/confirm", views.question_upload_confirm, name="question_upload_confirm"),
    
    path("collection/from_questions", login_required(views.CreateCollectionView.as_view()), name="collection_from_questions"),
    path("collection/all", login_required(views.collection_all), name="collection_all"),
    
    path("collection/<int:pk>", DetailView.as_view(model=Collection, template_name="QuizApp/collection/collection_detail.html")),
    
    path("", views.index, name="index"),
    
    path("test", views.test_view, name="test_page")
   
]