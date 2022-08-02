from django.conf import settings
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from core.projects.models import Project


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email,and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        try:
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_staffuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """User custom class"""

    email = models.EmailField(max_length=60, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # a admin user; non super-user
    is_superuser = models.BooleanField(default=False)  # a superuser

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Email & Password are required by default.

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self


class Permission(models.TextChoices):
    READONLY = 'R', _('ReadOnly')
    READANDWRITE = 'RW', _('ReadAndWrite')


class Role(models.TextChoices):
    AUTHOR = 'A', _('Author')
    CONTRIBUTOR = 'C', _('Contributor')


class Contributor(models.Model):
    """Contributor class - through class between User and Project"""

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    permission = models.CharField(max_length=2, choices=Permission.choices, default=Permission.READANDWRITE)
    # Définition de la permission floue dans l'énoncé du projet.
    # Nous appliquons par définition ici READANDWRITE car tous les cas sont déjà couverts par le rôle
    role = models.CharField(max_length=1, choices=Role.choices, default=Role.CONTRIBUTOR)

    class Meta:
        unique_together = ('user', 'project',)
