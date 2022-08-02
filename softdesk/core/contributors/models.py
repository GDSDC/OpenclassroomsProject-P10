from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.projects.models import Project

class ContributorPermission(models.TextChoices):
    READONLY = 'R', _('ReadOnly')
    READANDWRITE = 'RW', _('ReadAndWrite')


class ContributorRole(models.TextChoices):
    AUTHOR = 'A', _('Author')
    CONTRIBUTOR = 'C', _('Contributor')


class Contributor(models.Model):
    """Contributor class - through class between User and Project"""

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    permission = models.CharField(max_length=2, choices=ContributorPermission.choices, default=ContributorPermission.READANDWRITE)
    # Définition de la permission floue dans l'énoncé du projet.
    # Nous appliquons par définition ici READANDWRITE car tous les cas sont déjà couverts par le rôle
    role = models.CharField(max_length=1, choices=ContributorRole.choices, default=ContributorRole.CONTRIBUTOR)

    class Meta:
        unique_together = ('user', 'project',)