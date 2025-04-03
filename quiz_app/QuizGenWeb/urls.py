from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index_gen"),
    path("wizard/files", views.wizard_files, name="wizard_files"),
    path("wizard/params", views.wizard_params, name="wizard_params"),
    path("wizard/confirm", views.wizard_confirm, name="wizard_confirm"),
    path("wizard/download", views.wizard_download, name="wizard_download"),
    path("edit/file", views.edit_select_files, name="edit_file_select"),
]
