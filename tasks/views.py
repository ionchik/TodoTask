from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from tasks.forms import TaskForm
from tasks.models import Task


def index(request):
    tasks = []
    if request.user.is_authenticated:
        tasks = Task.objects.filter(owner=request.user).order_by('deadline')
    context = {'tasks': tasks}
    return render(request, 'tasks/index.html', context)

@login_required
def task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if task.owner != request.user:
        raise Http404
    return render(request, 'tasks/task.html', {'object': task})

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.owner = request.user
            new_task.save()
            return redirect('/')
    else:
        form = TaskForm()
    return render(request, 'tasks/create_task.html', {'form': form})

@login_required
def change_status(request, task_id):
    task = Task.objects.get(id=task_id)
    if task.owner != request.user:
        raise Http404
    if task:
        if request.method == 'POST':
            task.completed = not task.completed
            task.save()
            return JsonResponse({'status': 'success', 'completed': task.completed})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if task.owner != request.user:
        raise Http404
    if task:
        task.delete()
    return redirect("/")

@login_required
def edit_task(request, task_id):
    task_entity = Task.objects.get(id=task_id)
    if task_entity.owner != request.user:
        raise Http404
    if request.method != 'POST':
        form = TaskForm(instance=task_entity)
    else:
        form = TaskForm(instance=task_entity, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks:task', task_id=task_entity.id)
    context = {'task': task_entity, 'form': form}
    return render(request, 'tasks/edit_task.html', context)