from django.shortcuts import render

from quiz.models import Quiz

def index(request):
    return render(request, "quiz/index.html", context={"app": "Quiz"})

def choose(request):
    return render(request, "quiz/choose.html", context={})

def quiz(request):
    # Get the questions
    questions = Quiz.objects.first()
    # Processing answers
    answers = {}
    if request.method == "POST":
        print(request.POST)
        for q in questions.JSON:
            if q["type"] == "single" or q["type"] == "multiple":
                selected = [
                    int(x.split("_")[-1])-1 
                    for x in request.POST 
                    if x.startswith(q["id"])
                ]
                key = [0]*len(q["options"])
                for i in selected:
                    key[i] = 1
                print(key)
                print(q["correct"])
                print()
    context = {
        "questions": []
    }
    if questions:
        context["questions"] = questions.JSON
    return render(request, "quiz/quiz.html", context=context)
