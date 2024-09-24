from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(null=True)
    completed = models.BooleanField(default=False)
    priority = models.IntegerField(choices=[(1, 'Низкий'), (2, 'Средний'), (3, 'Высокий')], default=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
