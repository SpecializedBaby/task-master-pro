from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from task_manager.forms import TaskForm, WorkerCreationForm
from task_manager.models import TaskType, Worker, Position


class TaskFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.task_type = TaskType.objects.create(name="Development")
        cls.worker1 = get_user_model().objects.create_user(username="testuser1", password="password123")
        cls.worker2 = get_user_model().objects.create_user(username="testuser2", password="password123")

    def test_task_form_valid(self):
        form_data = {
            "name": "Test Task",
            "description": "Test description",
            "deadline": date(2024, 6, 3),
            "is_completed": False,
            "priority": "Medium",
            "task_type": self.task_type,
            "assignees": [self.worker1.id, self.worker2.id],
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

        self.assertEqual(form.cleaned_data["name"], form_data["name"])
        self.assertEqual(form.cleaned_data["description"], form_data["description"])
        self.assertEqual(form.cleaned_data["deadline"], form_data["deadline"])
        self.assertEqual(form.cleaned_data["is_completed"], form_data["is_completed"])
        self.assertEqual(form.cleaned_data["priority"], form_data["priority"])
        self.assertEqual(form.cleaned_data["task_type"], form_data["task_type"])
        self.assertEqual(list(form.cleaned_data["assignees"].values_list('id', flat=True)), form_data["assignees"])

    def test_task_form_invalid(self):
        form_data = {
            "name": "",
            "description": "Test description",
            "deadline": "2024-12-31",
            "is_completed": False,
            "priority": "Medium",
            "task_type": self.task_type.id,
            "assignees": [self.worker1.id, self.worker2.id],
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())


class WorkerCreationFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.position = Position.objects.create(name="SMM")

    def test_worker_creation_form_valid(self):
        form_data = {
            "username": "testuser",
            "position": self.position,
            "first_name": "First name",
            "last_name": "Last name",
            "password1": "Password123!",
            "password2": "Password123!",

        }
        form = WorkerCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
