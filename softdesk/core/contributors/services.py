from typing import Optional

from core.contributors.models import Contributor
from core.projects.models import Project
from core.users.models import User


def is_contributor(project: Project, contributor: User, with_role: Optional = None) -> bool:
    """Function that check if the user is a contributor of the project"""
    # if author
    if with_role:
        return Contributor.objects.filter(project=project, user=contributor, role=with_role).exists()
    # if not author
    else:
        return Contributor.objects.filter(project=project, user=contributor).exists()
