from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task

def register(request):
    if request.user.is_authenticated:
        return redirect("task_list")
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your account is ready. Welcome!")
            return redirect("task_list")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)
        status = self.request.GET.get("status", "all")
        query = self.request.GET.get("q", "").strip()
        if status == "pending":
            queryset = queryset.filter(completed=False)
        elif status == "completed":
            queryset = queryset.filter(completed=True)
        if query:
            from django.db.models import Q
            queryset = queryset.filter(Q(title__icontains=query) | Q(description__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_tasks = Task.objects.filter(user=self.request.user)
        context["total_count"] = all_tasks.count()
        context["pending_count"] = all_tasks.filter(completed=False).count()
        context["completed_count"] = all_tasks.filter(completed=True).count()
        context["current_status"] = self.request.GET.get("status", "all")
        context["search_query"] = self.request.GET.get("q", "")
        return context

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["title", "description", "due_date"]
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Task added successfully.")
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ["title", "description", "due_date"]
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task_list")

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Task updated successfully.")
        return super().form_valid(form)

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("task_list")

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Task deleted.")
        return super().form_valid(form)

@login_required
def complete_task(request, pk):
    if request.method != "POST":
        return redirect("task_list")
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.completed = not task.completed
    task.save(update_fields=["completed"])
    messages.success(request, "Task status updated.")
    return redirect("task_list")
