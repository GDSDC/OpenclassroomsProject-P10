from typing import Optional

from django.core.exceptions import ObjectDoesNotExist

from core.projects.models import Project
from core.users.models import ContributorRole, User, Contributor


# ----------- GETTING PROJECT BY ID ------------------

def project_exists(project_id: int) -> bool:
    """Function that check if the project exists in database"""
    # TODO remove me

    return Project.objects.filter(id=project_id).exists()


def get_project(project_id: int) -> Optional[Project]:
    """Function that check if the project exists in database"""
    try:
        return Project.objects.get(id=project_id)
    except ObjectDoesNotExist:
        return None


def is_contributor(project: Project, contributor: User, with_role: Optional[ContributorRole] = None) -> bool:
    """Function that check if the user is a contributor of the poject"""
    return Contributor.objects.filter(project_id=project, user_id=contributor, role=with_role).exists()


# def is_author(project: Project, contributor: User) -> bool:
#     """Function that check if the user is a contributor of the poject"""
#     return is_contributor(project, contributor, with_role=ContributorRole.AUTHOR)
