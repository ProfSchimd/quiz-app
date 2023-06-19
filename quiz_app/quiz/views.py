from django.shortcuts import render
from .models import Assignment

from quiz.models import Attempt, Quiz

def index(request):
    context = {
        "assignments": []
    }
    # If logged in, show available assignments
    if request.user.is_authenticated:
        context["assignments"] = Assignment.objects.all().filter(active=True)
    return render(request, "quiz/index.html", context=context)

def start(request):
    if not request.method == "POST" or not request.POST["assignSelect"]:
        return render(request, "quiz/error.html", context={
            "message": "It looks like you haven't submitted to an assignment"
        })
    
    current_user = request.user
    # TODO: Solve not-logged or unauthorized users
        
    # retrieve the assignment
    assignment_id = int(request.POST["assignSelect"])
    assignment = Assignment.objects.get(id=assignment_id)
    
    # Retrieve user attempts
    attempts = Attempt.objects.filter(user=current_user, assignment=assignment)
    
    context = {
        "assignment": assignment,
        "attempts": attempts
    }
    return render(request, "quiz/start.html", context=context)

def quiz(request):
    # Get the questions
    questions = Quiz.objects.first()
    # Processing answers
    answers = {}
    if request.method == "POST":
        # print("\n".join([f"{k}: {v}, {request.POST.getlist(k)}" for k, v in request.POST.items()]))
        answer = {}
        for q in questions.JSON:
            if q["type"] == "single" or q["type"] == "multiple":
                # List of selected options.
                # Checkboxes and radios have name on the form 001_3
                # indicating ID and position. This code splits the
                # two and yields the second part when id = q["id"]
                selected = [int(x)-1 for x in request.POST.getlist(q["id"])]
                key = [0]*len(q["options"])
                for i in selected:
                    key[i] = 1
                answer[q["id"]] = key
                
    context = {
        "questions": []
        
    }
    if questions:
        context["questions"] = questions.JSON
    
    return render(request, "quiz/quiz.html", context=context)
