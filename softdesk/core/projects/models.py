from django.db import models
from django.conf import settings

PROJECT_PERMISSIONS = [('EXEMPLE_A_COMPLETER','IDEM')]
#TODO : remplir les permissions possibles pour les contributeurs dans le cadre d'un projet au format valide

class Project(models.Model):
    """Projects class"""

    title = models.CharField(max_length=60, blank=True)
    description = models.CharField(max_length=512, blank=True)
    type = models.CharField(max_length=60, blank=True)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
