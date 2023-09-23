from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.views.generic.edit import CreateView

from .models import Question, Subject, Tag

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
    
class CreateQuestionView(PermissionRequiredMixin, CreateView):
    permission_required = "quizapp.add_quiz"
    model = Question
    fields = ["question_type", "weight", "text_and_keys", "subject", "tags"]
    template_name = "QuizApp/create_quiz.html"
    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
    

# Create your views here.
def index(request):
    return render(template_name="QuizApp/index.html", context={}, request=request)

def create_question(request):
    if request.method == "POST":
        print(request.POST)
    return render(template_name="QuizApp/create_question.html", context={}, request=request)