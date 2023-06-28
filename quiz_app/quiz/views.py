from datetime import datetime

from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from quiz.models import Attempt, Assignment, Quiz

def index(request):
    context = {
        "assignments": []
    }
    # If logged in, show available assignments
    if request.user.is_authenticated:
        context["assignments"] = Assignment.objects.all().filter(active=True)
    return render(request, "quiz/index.html", context=context)

def start(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    # Retrieve user attempts
    attempts = Attempt.objects.filter(user=request.user, assignment=assignment)
    context = {
        "assignment": assignment,
        "attempts": attempts
    }
    return render(request, "quiz/start.html", context=context)

def create(request, assignment_id):
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        raise PermissionDenied
    quiz = Quiz.objects.all().first()
    assignment = Assignment.objects.all().filter(id=assignment_id).first()
    if not assignment:
        return render(request, "quiz/error.html", context={
            "message": "Assignment creation error"
        })
    attempt = Attempt(
        user = request.user,
        assignment=assignment,
        quiz=quiz,
        start=datetime.now()
    )
    attempt.save()
    print(attempt)
    url = reverse('quiz', kwargs={'attempt_id': attempt.id})
    return redirect(url)

def quiz(request, attempt_id=0):
    print("ATT#: ", attempt_id)
    # create new attempt
    if attempt_id == 0:
        print("TODO Create new attempt for", request.user)
    attempt = Attempt.objects.all().filter(id=attempt_id).first()
    if (attempt is None) or (attempt.user != request.user):
        print(attempt)
        print(request.user)
        return render(request, "quiz/error.html", context={
            "message": "Invalid assignment"
        })
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
        "attempt": attempt_id,
        "questions": []
        
    }
    if questions:
        context["questions"] = questions.JSON
    
    return render(request, "quiz/quiz.html", context=context)

def save(request, attempt_id):
    print(f"SAVE: {attempt_id}")
    # ToDo:
    return redirect(reverse("quiz", kwargs={"attempt_id": attempt_id}))

def delete(request, attempt_id):
    print(f"DELETE: {attempt_id}")
    attempt = get_object_or_404(Attempt, pk=attempt_id)
    if request.user != attempt.user:
        raise PermissionDenied()
    assignment_id = attempt.assignment.id
    return redirect(reverse("start", kwargs={"assignment_id": assignment_id}))
