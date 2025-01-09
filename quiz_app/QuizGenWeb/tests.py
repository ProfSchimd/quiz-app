from django.test import Client, TestCase
from django.urls import reverse
from QuizApp.models import Subject

from .models import QuizFile

class ClassFileTest(TestCase):
    def setUp(self):
        subject = Subject.objects.create(name="Informatica", short_name="INF", description=None)
        QuizFile.objects.create(path="/tmp/inf.json", subject=subject)
        
    def test_quiz_file_name(self):
        qf = QuizFile.objects.get(path="/tmp/inf.json")
        self.assertEqual(qf.name(), "inf", "name doesn't match")
        
    def test_quiz_file_str(self):
        path = "/tmp/inf.json"
        qf = QuizFile.objects.get(path=path)
        self.assertEqual(qf.__str__(), f"inf ({path})")
        
class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        
    def test_wizard_confirm_view(self):
        params = {
                "n": 10,
                "tracks": 3,
                "seed": "123",
                "render": "html",
            }
        response = self.client.post(
            reverse("wizard_confirm"),
            {
                "file_ids": [1,2],
                **params,
            },
        )
        self.assertEqual(response.status_code, 200, "Status is not 200")
        self.assertTemplateUsed(response, "QuizGenWeb/wizard_confirm.html")
        for k, v in params.items():
            self.assertEqual(response.context[k], v)
            self.assertContains(
                response, 
                f'<input type="hidden" name="{k}" value="{params[k]}">',
                html=True
            )
            self.assertEqual(str(self.client.session[k]), str(v))
        