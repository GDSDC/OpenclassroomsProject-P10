from django.db import models
from django.conf import settings
from core.users.models import User


class Project(models.Model):
    """Projects class"""

    title = models.CharField(max_length=60, unique=True)
    description = models.CharField(max_length=512, blank=True)
    type = models.CharField(max_length=60, blank=True)
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def is_author(self, author: User) -> bool:
        """Function that check if the user is the author of the poject"""
        return self.author_user == author