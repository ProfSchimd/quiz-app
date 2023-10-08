from django import forms

from .models import Subject

class UploadFileForm(forms.Form):
    name = forms.CharField(max_length=50)
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        empty_label="Select a subject",
        required=False
    )
    file = forms.FileField()
    
class QuestionForm(forms.Form):
    q_id = forms.CharField(max_length=255)