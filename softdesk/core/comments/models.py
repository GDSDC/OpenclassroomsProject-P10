from django.db import models
from django.conf import settings
from core.issues.models import Issue


class Comment(models.Model):
    """Comments class"""

    description = models.CharField(max_length=512, blank=True)
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                    related_name='comment_author')
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
