import json
import random
from typing import Any

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import CreateView

from .forms import QuestionForm, UploadFileForm
from .models import Collection, Question, Subject, Tag

from pyquiz.pyquiz import parse_question_json, create_quiz

# Views implemented with Django helpers
class CreateTagView(PermissionRequiredMixin, CreateView):
    permission_required = "QuizApp.add_tag"
    model = Tag
    fields = ["name", "description"]
    template_name="QuizApp/create_tag.html"
    success_url = "/quizapp"
    

class CreateSubjectView(PermissionRequiredMixin, CreateView):
    permission_required = "QuizApp.add_subject"
    model = Subject
    fields =["name", "short_name", "description"]
    template_name = "QuizApp/create_subject.html"
    success_url = "/quizapp"
    
class CreateCollectionView(PermissionRequiredMixin, CreateView):
    permission_required = "QuizApp.add_collection"
    model = Collection
    fields = ["name", "description", "topic", "subject", "is_virtual"]
    template_name = "QuizApp/collection/create_collection.html"
    success_url="/"
    
    def form_valid(self, form):
        model = form.save()
        questions = questions_from_post(self.request.POST)
        print(self.request.POST)
        model.questions.set(questions)
        model.save()
        return super().form_valid(form)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = questions_from_post(self.request.POST)
        context["questions"] = questions
        return context
    
    

# Views requiring custom logic (w.r.t. Django helpers)
def index(request):
    print(type(request.user.get_group_permissions()))
    return render(template_name="QuizApp/index.html", context={}, request=request)


def question_show(request, q_id=0):
    if request.method == "POST":
        # TODO: Process request of "Question Creation" view
        print(request.POST)
    q: Question = get_object_or_404(Question, pk=q_id)
    form = QuestionForm(options=enumerate(q.text_and_keys["options"]))
    return render(
        template_name="QuizApp/question/question_n.html", 
        context={
            "q_id": q.id,
            "type": q.get_question_type_display(),
            "text": "<br>".join(q.text_and_keys["text"]) if q.get_question_type_display() == "Invertible" else q.text_and_keys["text"],
            "tags": [t.name for t in q.tags.all()],
            "form": form
        },
        request=request)
    
def question_list(request):
    query = Q()
    tag_list = request.GET.getlist("tag")
    if tag_list:
        for tag_name in tag_list:
            query |= Q(tags__name__iexact=tag_name)
    subject = request.GET.get("subject")
    if subject:
        query &= Q(subject__short_name__iexact=subject)
    questions = Question.objects.filter(query)
    return render(template_name="QuizApp/question/question_list.html", context={"questions": questions}, request=request)

def question_export(request):
    if request.method == "POST":
        # question_ids = [key.split("_")[1] for key in request.POST if key.startswith("id_")]
        # questions = Question.objects.filter(pk__in=question_ids)
        questions = questions_from_post(request.POST)
        response = HttpResponse(
            content_type="application/json",
            headers={"Content-Disposition": 'attachment; filename="export.json"'},
        )
        jsonQuestions = [q.to_json() for q in questions]
        if request.POST.get("random"):
            seed = request.POST.get("seed")
            random.seed(seed)
            
            jsonQuestions = create_quiz(parse_question_json(jsonQuestions), len(questions))
            jsonQuestions = [q.to_dict() for q in jsonQuestions]
        json.dump(jsonQuestions, response, ensure_ascii=False, indent=4)
        return response
    return redirect("question_show")

def question_create(request):
    if request.method == "POST":
        # TODO: Process request of "Question Creation" view
        print(request.POST)
    all_subjects = Subject.objects.all()
    context = {
        "types": Question.QUESTION_TYPE,
        "subjects": [(s.short_name, s.name) for s in all_subjects],
        }
    return render(template_name="QuizApp/create_question.html", context=context, request=request)

# TODO: This can be transformed into a form view
def question_upload(request):        
    form = UploadFileForm()
    return render(template_name="QuizApp/question/question_upload.html", context={"form": form}, request=request)

def question_upload_confirm(request):
    if request.method == "POST":
        # in case i find 'confirmed-data' this is definitely confirmed
        if request.POST.get("confirmed-data"):
            subject=Subject.objects.get(pk=int(request.POST.get("subject")))
            included_questions = []
            for k in request.POST.keys():
                if(k.startswith("q_")):
                    included_questions.append(k[2:])
            jsonData = json.loads(request.POST.get("confirmed-data"))
            for q in jsonData:
                if q["id"] in included_questions:
                    print(q["id"], q["type"])
                    # TODO: This changes for other type of question (e.g. fill)
                    text_and_key = {
                        "text": q["text"],
                        "options": q["options"],
                        "correct": q["correct"]
                    }
                            
                    # qModel = Question(
                    #     question_type=q["type"].upper(),
                    #     weight=int(q["weight"]),
                    #     subject=subject,
                    #     creator=request.user,
                    #     text_and_keys=text_and_key,
                    # )
                    # # Create tags that may not exist
                    # qModel.save()
                    # if q.get("tags"):
                    #     for tag in q["tags"]:
                    #         tag, _ = Tag.objects.get_or_create(name__iexact=tag, defaults={"name": tag})
                    #         qModel.tags.add(tag)
                    # qModel.save()
                    Question.add_or_update(
                        type=q["type"].upper(),
                        weight=int(q["weight"]),
                        subject=subject,
                        tags=q.get("tags"),
                        text_and_key = {
                            "text": q["text"],
                            "options": q["options"],
                            "correct": q["correct"]
                        },
                        creator=request.user,
                        update_tags=True,
                        id=None
                    )
            return redirect("question_show")
        
        # Process and render confirmation page
        file = request.FILES.get('file')
        if file:
            data = file.read()
            jsonData = json.loads(data)
            return render(
                template_name="QuizApp/question/question_upload_confirm.html",
                context={
                    "data": jsonData,
                    "rawData": json.dumps(jsonData),
                    "name": request.POST.get("name"),
                    "subject": request.POST.get("subject")
                },
                request=request
            )
    return redirect("question_upload")

def collection_from_questions(request):
    return redirect("index")

def questions_from_post(post):
    question_ids = [key.split("_")[1] for key in post if key.startswith("id_")]
    questions = Question.objects.filter(pk__in=question_ids)
    return questions
