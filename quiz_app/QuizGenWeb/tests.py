from django.test import Client, TestCase, SimpleTestCase
from django.urls import reverse
from QuizApp.models import Subject

import os
import shutil
from unittest.mock import patch

from .models import QuizFile
from .utils import make_temp_dir

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
        


CREATED_DIRS = []  # track dirs to clean up after each test


class MakeTempDirTestCase(SimpleTestCase):

    def tearDown(self):
        """Clean up any directories created during tests."""
        for path in CREATED_DIRS:
            if path and os.path.exists(path):
                shutil.rmtree(path, ignore_errors=True)
        CREATED_DIRS.clear()

    # ------------------------------------------------------------------ #
    # Happy path — named directory
    # ------------------------------------------------------------------ #

    def test_named_dir_is_created(self):
        """A directory with the given name must exist after the call."""
        path = make_temp_dir("my_test_dir")
        CREATED_DIRS.append(path)
        self.assertIsNotNone(path)
        self.assertTrue(os.path.isdir(path), f"Expected a directory at {path}")

    def test_named_dir_ends_with_given_name(self):
        """The returned path must end with the requested name."""
        path = make_temp_dir("custom_name")
        CREATED_DIRS.append(path)
        self.assertIsNotNone(path)
        self.assertTrue(
            path.endswith("custom_name"),
            f"Path '{path}' does not end with 'custom_name'",
        )

    def test_named_dir_returns_string(self):
        """Return value must be a string (not bytes, Path, etc.)."""
        path = make_temp_dir("string_check")
        CREATED_DIRS.append(path)
        self.assertIsInstance(path, str)

    # ------------------------------------------------------------------ #
    # Happy path — auto-generated name
    # ------------------------------------------------------------------ #

    def test_no_name_creates_a_directory(self):
        """Calling with no argument must still create a real directory."""
        path = make_temp_dir()
        CREATED_DIRS.append(path)
        self.assertIsNotNone(path)
        self.assertTrue(os.path.isdir(path), f"Expected a directory at {path}")

    def test_no_name_returns_string(self):
        """Return value must be a string when no name is supplied."""
        path = make_temp_dir()
        CREATED_DIRS.append(path)
        self.assertIsInstance(path, str)

    def test_no_name_generates_non_empty_dirname(self):
        """The auto-generated directory name must not be empty."""
        path = make_temp_dir()
        CREATED_DIRS.append(path)
        self.assertIsNotNone(path)
        dirname = os.path.basename(path)
        self.assertTrue(len(dirname) > 0, "Auto-generated dir name is empty")

    def test_two_calls_without_name_produce_different_paths(self):
        """Two no-arg calls must not collide."""
        path1 = make_temp_dir()
        path2 = make_temp_dir()
        CREATED_DIRS.extend([path1, path2])
        self.assertNotEqual(path1, path2)

    # ------------------------------------------------------------------ #
    # Return value semantics
    # ------------------------------------------------------------------ #

    def test_returns_absolute_path(self):
        """The returned path must be absolute."""
        path = make_temp_dir("abs_path_test")
        CREATED_DIRS.append(path)
        self.assertIsNotNone(path)
        self.assertTrue(os.path.isabs(path), f"Path '{path}' is not absolute")

    def test_returns_none_on_os_error(self):
        """If the OS raises an error, the function must return None."""
        with patch("os.makedirs", side_effect=OSError("permission denied")):
            result = make_temp_dir("will_fail")
        self.assertIsNone(result)

    def test_returns_none_on_unexpected_exception(self):
        """Any unexpected exception during creation must also return None."""
        with patch("os.makedirs", side_effect=Exception("unexpected")):
            result = make_temp_dir("unexpected_fail")
        self.assertIsNone(result)

    # ------------------------------------------------------------------ #
    # Idempotency / edge cases
    # ------------------------------------------------------------------ #

    def test_same_name_twice_does_not_raise(self):
        """Calling with the same name twice must not crash the process."""
        path1 = make_temp_dir("duplicate_dir")
        path2 = make_temp_dir("duplicate_dir")
        CREATED_DIRS.extend([path1, path2])
        # Both calls should succeed (exist_ok semantics) or second returns None —
        # either is acceptable, but neither may raise.
        # If both succeed, paths must be equal.
        if path1 is not None and path2 is not None:
            self.assertEqual(path1, path2)

    def test_name_with_spaces_handled(self):
        """A name containing spaces must not cause an unhandled crash."""
        path = make_temp_dir("dir with spaces")
        CREATED_DIRS.append(path)
        # Either succeeds and returns a real dir, or gracefully returns None.
        if path is not None:
            self.assertTrue(os.path.isdir(path))