from django.urls import path
from .views import task, index, create_task, change_status, delete_task, edit_task

app_name = 'tasks'
urlpatterns = [
    path('', index, name='index'),
    path('<int:task_id>/', task, name='task'),
    path('create/', create_task, name='create_task'),
    path('<int:task_id>/delete', delete_task, name='delete_task'),
    path('<int:task_id>/edit', edit_task, name='edit_task'),
    path('<int:task_id>/change_status/', change_status, name='change_status'),
]