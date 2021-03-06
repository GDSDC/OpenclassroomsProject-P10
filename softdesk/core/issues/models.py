from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from core.projects.models import Project


class Issue(models.Model):
    """Issues class"""

    class Tag(models.TextChoices):
        BUG = 'B', _('Bug')
        TASK = 'T', _('Task')
        IMPROVEMENT = 'I', _('Improvement')

    class Priority(models.TextChoices):
        LOW = 'L', _('Low')
        MEDIUM = 'M', _('Medium')
        HIGH = 'H', _('High')

    class Status(models.TextChoices):
        TODO = 'TD', _('To Do')
        INPROGRESS = 'P', _('In Progress')
        DONE = 'D', _('Done')

    title = models.CharField(max_length=60)
    desc = models.CharField(max_length=512, blank=True)
    tag = models.CharField(max_length=1, choices=Tag.choices)
    priority = models.CharField(max_length=1, choices=Priority.choices)
    project_id = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.TODO)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL,on_delete=models.SET_NULL, null=True,
                                       related_name='author')
    assignee_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                         related_name='assignee')
    created_time = models.DateTimeField(auto_now_add=True)
