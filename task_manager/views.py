from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from task_manager.forms import (
    TaskForm,
    WorkerCreationForm,
    TaskSearchForm,
    TaskTypeSearchForm,
)
from task_manager.models import Worker, Task, TaskType, Position


def index(request):
    num_workers = Worker.objects.count()
    num_tasks = Task.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_workers": num_workers,
        "num_tasks": num_tasks,
        "num_visits": num_visits + 1,
    }

    return render(request, "task_manager/index.html", context=context)


class WorkerTaskListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    template_name = "task_manager/worker_task_list.html"
    context_object_name = "worker_tasks"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerTaskListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = self.request.user.task_set.all().select_related("task_type")
        form = TaskSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get("name", "")

        if name:
            return queryset.filter(name__icontains=name)
        return queryset


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")

    def get_initial(self):
        initial = super().get_initial()
        referer = self.request.META.get("HTTP_REFERER")
        if "my-tasks" in referer:
            initial["assignees"] = [self.request.user]
        return initial


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:task-list")


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    paginate_by = 5
    template_name = "task_manager/task_type_list.html"
    context_object_name = "task_type_list"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskTypeSearchForm(
            initial={
                "name": name,
            }
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get("name", "")
        if name:
            return queryset.filter(name__icontains=name)
        return queryset


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    template_name = "task_manager/task_type_form.html"
    success_url = reverse_lazy("task_manager:task-type-list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    template_name = "task_manager/task_type_form.html"
    success_url = reverse_lazy("task_manager:task-type-list")


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    template_name = "task_manager/task_type_confirm_delete.html"
    success_url = reverse_lazy("task_manager:task-type-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        first_name = self.request.GET.get("firs_name", "")
        context["search_form"] = TaskTypeSearchForm(
            initial={
                "firs_name": first_name,
            }
        )
        return context

    def get_queryset(self):
        queryset = Worker.objects.select_related("position")
        first_name = self.request.GET.get("first_name", "")
        if first_name:
            return queryset.filter(first_name__icontains=first_name)
        return queryset


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    queryset = Worker.objects.all().prefetch_related("task_set__task_type")
    template_name = "task_manager/worker_detail.html"

    def get_context_data(self, **kwargs):
        context = super(WorkerDetailView, self).get_context_data(**kwargs)
        worker = self.object
        all_tasks = Task.objects.filter(assignees=worker)
        count_of_tasks = all_tasks.count()
        count_of_completed_tasks = all_tasks.filter(is_completed=True).count()
        count_of_active_tasks = all_tasks.filter(is_completed=False).count()

        context.update(
            {
                "worker": worker,
                "count_of_tasks": count_of_tasks,
                "count_of_completed_tasks": count_of_completed_tasks,
                "count_of_active_tasks": count_of_active_tasks,
            }
        )
        return context


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("task_manager:worker-list")


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("task_manager:worker-list")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("task_manager:worker-list")


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PositionListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskTypeSearchForm(
            initial={
                "name": name,
            }
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get("name", "")
        if name:
            return queryset.filter(name__icontains=name)
        return queryset


class PositionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Position


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("task_manager:position-list")


class ToggleAssignToTaskView(LoginRequiredMixin, generic.View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        worker = Worker.objects.get(id=request.user.id)
        task = Task.objects.get(id=pk)

        if task in worker.task_set.all():
            worker.task_set.remove(pk)
        else:
            worker.task_set.add(pk)

        return redirect("task_manager:task-detail", pk=pk)
