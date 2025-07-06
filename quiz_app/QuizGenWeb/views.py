from django.shortcuts import get_object_or_404, redirect, render
from pyquiz import pyquiz

from .models import QuizFile


def index(request):
    return render(request=request, template_name="QuizGenWeb/index.html")


def process_file(file):
    questions = pyquiz.load_questions([file.path])
    return {
        "id": file.id,
        "path": file.path,
        "name": file.name(),
        "count": len(questions),
        "types": {
            "single": len([q for q in questions if q["type"] == "single"]),
            "multiple": len([q for q in questions if q["type"] == "multiple"]),
            "invertible": len(
                [q for q in questions if q["type"] == "invertible"]
            ),
            "fill": len([q for q in questions if q["type"] == "fill"]),
        },
    }


def wizard_files(request):
    # Load selected files from the session
    selected_files = request.session.get("selected_files", [])
    selected_file_ids = set([int(i) for i in selected_files])

    if request.method == "POST":
        # Add checked files
        if "file_ids" in request.POST:
            selected_file_ids |= set(
                [int(i) for i in request.POST.getlist("file_ids")]
            )
        # Removed deleted files
        if "delete_file" in request.POST:
            selected_file_ids -= {int(request.POST["delete_file"])}

    # Update the session and build the context
    request.session["selected_files"] = list(selected_file_ids)
    selected_files = QuizFile.objects.filter(id__in=selected_file_ids)
    context = {
        "files": QuizFile.objects.all(),
        "selected_files": [process_file(file) for file in selected_files],
        "subjects": list(set(str(file.subject) for file in selected_files)),
    }
    return render(request, "QuizGenWeb/wizard_files.html", context=context)


def wizard_params(request):
    if request.method == "POST":
        # Get selected files from the POST request
        selected_file_ids = request.POST.getlist("file_ids")
        selected_files = QuizFile.objects.filter(id__in=selected_file_ids)
        
        # Prepare the context with the selected file URLs
        context = {
            "selected_files": selected_files,
            "n": request.session.get("n") or None,
            "tracks": request.session.get("n") or None,
            "seed": request.session.get("seed") or None,
        }
        return render(
            request=request,
            template_name="QuizGenWeb/wizard_params.html",
            context=context,
            
        )

    # Redirect to `wizard_files` if accessed via GET
    return redirect("wizard_files")


def wizard_confirm(request):
    if request.method == "POST":
        # We should check that all parameters are given, otherwise we should
        # redirect to previous 
        selected_file_ids = request.POST.getlist("file_ids")
        selected_files = QuizFile.objects.filter(id__in=selected_file_ids)
        context = {
            "selected_files": [process_file(file) for file in selected_files],
            "file_ids": [int(id) for id in request.POST.getlist("file_ids")],
            "n": int(request.POST.get("n", -1)),
            "tracks": int(request.POST.get("tracks", 1)),
            "seed": request.POST.get("seed"),
            "render": request.POST.get("render"),
        }
        request.session["n"] = context["n"]
        request.session["tracks"] = context["tracks"]
        request.session["seed"] = context["seed"]
        request.session["render"] = context["render"]
        return render(
            request=request,
            template_name="QuizGenWeb/wizard_confirm.html",
            context=context,
        )
    return redirect("wizard_files")


def wizard_download(request):
    if request.method == "POST":
        # Create a destination directory, prepare args, and use pyquiz
        # script from the CLI app.
        selected_file_ids = request.POST.getlist("file_ids")
        selected_files = QuizFile.objects.filter(id__in=selected_file_ids)
        args = {
            "input": [file.path for file in selected_files],
            "destination": "/tmp",
            "n": int(request.POST.get("n")),
            "seed": request.POST.get("seed"),
            "tracks": int(request.POST.get("tracks")),
            "render": request.POST.get("render"),
            "output": "text",
            "solution": "solution",
            "template": None,
            "render_meta": False,
            "include_hidden": False,
            "test": 0,
            "verbosity": 0, 
        }
        from argparse import Namespace
        ns = Namespace(**args)
        info = pyquiz.run(ns)
        pyquiz.print_output(info, 3, "/tmp/info.txt")
        context = {}
        return render(
            request=request,
            template_name="QuizGenWeb/wizard_download.html",
            context=context,
        )
    return redirect("wizard_files")


def edit_select_files(request):
    context = {
        "files": QuizFile.objects.all(),
    }
    return render(request, "QuizGenWeb/edit_file_select.html", context=context)

def edit_show_questions(request):
    if (not request.method == "POST") or (not request.POST.get("file_ids")) :
        return redirect("edit_file_select")
    selected_files=request.POST.getlist("file_ids")
    files = []
    for f in QuizFile.objects.filter(id__in=selected_files):
        files.append({
            "name": f.name,
            "id": f.id,
            "questions": pyquiz.json_to_questions(f.path)
        })
    context = {
        "files": files
    }
    return render(request, "QuizGenWeb/edit_questions_show.html", context=context)

def edit_question(request, file, qid):
    if request.method == "POST":
        print(request.POST)
    quiz_file = get_object_or_404(QuizFile, pk=file)
    print(quiz_file)
    if not quiz_file:
        print('ErRoR¡')
    context = {
        "question": {
            "q_id": qid,
            "type": "single",
            "options": [1,2,3],
        }
    }
    return render(request, "QuizGenWeb/edit_question.html", context=context)