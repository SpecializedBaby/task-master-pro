from django.urls import path

from task_manager.views import index, TaskListView

urlpatterns = [
    path("", index, name="index"),
]

app_name = "task_manager"
