# task_manager/tests/test_models.py
from django.contrib.auth import get_user_model
from django.test import TestCase
from task_manager.models import Task, TaskType, Worker, Position


class TaskModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a TaskType and Worker for testing
        cls.task_type = TaskType.objects.create(name="Development")
        cls.worker = Worker.objects.create(username="testuser", password="password123")

        # Create a Task for testing
        cls.task = Task.objects.create(
            name="Test Task",
            description="Test description",
            deadline="2024-12-31",
            is_completed=False,
            priority="Medium",
            task_type=cls.task_type,
        )
        cls.task.assignees.add(cls.worker)

    def test_task_creation(self):
        self.assertEqual(self.task.name, "Test Task")
        self.assertEqual(self.task.description, "Test description")
        self.assertEqual(self.task.deadline, "2024-12-31")
        self.assertFalse(self.task.is_completed)
        self.assertEqual(self.task.priority, "Medium")
        self.assertEqual(self.task.task_type, self.task_type)
        self.assertIn(self.worker, self.task.assignees.all())


class WorkerModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.position = Position.objects.create(name="CEO")
        cls.worker = get_user_model().objects.create_user(
            username="username_test",
            password="1qazcde3",
            first_name="First name",
            last_name="Last name",
            position=cls.position
        )

    def test_worker_creation(self):
        self.assertEqual(self.worker.username, "username_test")
        self.assertEqual(self.worker.position.name, "CEO")
        self.assertTrue(self.worker.check_password("1qazcde3"))

    def test_worker_str(self):
        self.assertEqual(str(self.worker), f"{self.worker.first_name} {self.worker.last_name}")
