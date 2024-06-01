# task_manager/tests/test_views.py
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from task_manager.models import Task, TaskType, Worker


class PublicTaskManagerTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        response = self.client.get("task_manager:index")
        self.assertEqual(response.status_code, 200)

    def test_login_required(self):
        response = self.client.get("task_manager:worker-list")
        self.assertNotEqual(response.status_code, 200)


class TaskViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.task_type = TaskType.objects.create(name="Development")
        cls.worker = get_user_model().objects.create_user(
            username="testuser", password="Password123!"
        )
        cls.task = Task.objects.create(
            name="Test Task",
            description="Test description",
            deadline="2024-12-31",
            is_completed=False,
            priority="Medium",
            task_type=cls.task_type,
        )
        cls.task.assignees.add(cls.worker)

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="Pasword123!"
        )
        self.client.force_login(self.user)

    def test_task_list_view(self):
        response = self.client.get(reverse("task_manager:task-list"))
        self.assertEqual(response.status_code, 200)
        task_list = Task.objects.all()
        self.assertEqual(list(response.context["task_list"]), list(task_list))

    def test_task_detail_view(self):
        response = self.client.get(
            reverse("task_manager:task-detail", args=[self.task.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Task")
