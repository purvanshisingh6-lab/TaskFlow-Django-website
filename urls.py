from django.urls import path
from . import views

urlpatterns = [
    path("", views.TaskListView.as_view(), name="task_list"),
    path("tasks/add/", views.TaskCreateView.as_view(), name="task_create"),
    path("tasks/<int:pk>/edit/", views.TaskUpdateView.as_view(), name="task_update"),
    path("tasks/<int:pk>/delete/", views.TaskDeleteView.as_view(), name="task_delete"),
    path("tasks/<int:pk>/complete/", views.complete_task, name="complete_task"),
]
