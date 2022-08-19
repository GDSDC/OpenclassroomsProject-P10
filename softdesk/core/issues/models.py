from django.db import models
from django.conf import settings
from core.projects.models import Project


class Issue(models.Model):
    """Issues class"""

    class Tag(models.TextChoices):
        BUG = 'BUG', 'Bug'
        TASK = 'TASK', 'Task'
        IMPROVEMENT = 'IMPROVEMENT', 'Improvement'

    class Priority(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'

    class Status(models.TextChoices):
        TODO = 'TODO', 'To Do'
        INPROGRESS = 'INPROGRESS', 'In Progress'
        DONE = 'DONE', 'Done'

    title = models.CharField(max_length=60, unique=True)
    desc = models.CharField(max_length=512, blank=True)
    tag = models.CharField(max_length=12, choices=Tag.choices)
    priority = models.CharField(max_length=6, choices=Priority.choices)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.TODO)
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                    related_name='author')
    assignee_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                      related_name='assignee')
    created_time = models.DateTimeField(auto_now_add=True)
