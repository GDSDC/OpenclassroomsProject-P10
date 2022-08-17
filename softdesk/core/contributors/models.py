from django.conf import settings
from django.db import models
from core.projects.models import Project





class Contributor(models.Model):
    """Contributor class - through class between User and Project"""

    class Permission(models.TextChoices):
        READONLY = 'READONLY', 'ReadOnly'
        READANDWRITE = 'READANDWRITE', 'ReadAndWrite'

    class Role(models.TextChoices):
        AUTHOR = 'AUTHOR', 'Author'
        CONTRIBUTOR = 'CONTRIBUTOR', 'Contributor'

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    permission = models.CharField(max_length=12, choices=Permission.choices,
                                  default=Permission.READANDWRITE)
    # Définition de la permission floue dans l'énoncé du projet.
    # Nous appliquons par définition ici READANDWRITE car tous les cas sont déjà couverts par le rôle
    role = models.CharField(max_length=12, choices=Role.choices, default=Role.CONTRIBUTOR)

    class Meta:
        unique_together = ('user', 'project',)

    @property
    def role_name(self):
        return self.Role(self.role).name
