from .models import QuizFile
from pyquiz import pyquiz

from django.shortcuts import redirect, render


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
            "invertible": len([q for q in questions if q["type"] == "invertible"]),
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
            selected_file_ids |= set([int(i) for i in request.POST.getlist("file_ids")])
        # Removed deleted files
        if "delete_file" in request.POST:
            selected_file_ids -= {int(request.POST["delete_file"])}

    # Update the session and build the context
    request.session["selected_files"] = list(selected_file_ids)
    selected_files = QuizFile.objects.filter(id__in=selected_file_ids)
    context = {
        "files": QuizFile.objects.all(),
        "selected_files": [process_file(file) for file in selected_files],
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
        selected_file_ids = request.POST.getlist("file_ids")
        selected_files = QuizFile.objects.filter(id__in=selected_file_ids)
        # currently we use a workaround by inserting **POST. However,
        # this MUST be changed in the future to add parameters checking
        # and prevent security issues by sharing CRSF token.
        context = {
            "selected_files": [process_file(file) for file in selected_files],
            **request.POST,
        }
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
        print(request.POST)
        selected_file_ids = request.POST.getlist("file_ids")
        selected_files = QuizFile.objects.filter(id__in=selected_file_ids)
        args = {
            "input": [file.path for file in selected_files],
            "destination": "/tmp",
            "n": int(request.POST.get("n"))
        }
        print(args)
        #pyquiz.run(args)
        context = {}
        return render(
            request=request,
            template_name="QuizGenWeb/wizard_download.html",
            context=context,
        )
    return redirect("wizard_files")
