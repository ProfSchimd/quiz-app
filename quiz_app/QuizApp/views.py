import json

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView

from .forms import UploadFileForm
from .models import Question, Subject, Tag

# Views implemented with Django helpers
class CreateTagView(PermissionRequiredMixin, CreateView):
    permission_required = "quizapp.add_tag"
    model = Tag
    fields = ["name", "description"]
    template_name="QuizApp/create_tag.html"
    success_url = "/quizapp"
    

class CreateSubjectView(PermissionRequiredMixin, CreateView):
    permission_required = "quizapp.add_subject"
    model = Subject
    fields =["name", "short_name", "description"]
    template_name = "QuizApp/create_subject.html"
    success_url = "/quizapp"

# Views requiring custom logic (w.r.t. Django helpers)
def index(request):
    return render(template_name="QuizApp/index.html", context={}, request=request)

def create_question(request):
    if request.method == "POST":
        # TODO: Process request of "Question Creation" view
        print(request.POST)
    return render(template_name="QuizApp/create_question.html", context={}, request=request)

def question_list(request):
    if request.method == "POST":
        # TODO: process request from the "Question List" view
        print(request.POST)
    questions = Question.objects.all()
    return render(template_name="QuizApp/question/question_list.html", context={"questions": questions}, request=request)
    
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
                            
                    qModel = Question(
                        question_type=q["type"].upper(),
                        weight=int(q["weight"]),
                        subject=subject,
                        creator=request.user,
                        text_and_keys=text_and_key,
                    )
                    # Create tags that may not exist
                    qModel.save()
                    if q["tags"]:
                        for tag in q["tags"]:
                            tag, _ = Tag.objects.get_or_create(name__iexact=tag, defaults={"name": tag})
                            qModel.tags.add(tag)
                    qModel.save()
            return redirect("question_upload")
        
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
