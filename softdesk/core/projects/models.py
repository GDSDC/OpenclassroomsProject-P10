from django.db import models
from django.conf import settings


class Project(models.Model):
    """Projects class"""

    title = models.CharField(max_length=60, unique=True)
    description = models.CharField(max_length=512, blank=True)
    type = models.CharField(max_length=60, blank=True)
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
