from typing import Optional
from django.core.exceptions import ObjectDoesNotExist
from core.projects.models import Project
from core.contributors.models import Contributor
from core.users.models import User


# ----------- GETTING PROJECT BY ID ------------------


def get_project(project_id: int) -> Optional[Project]:
    """Function that check if the project exists in database"""
    try:
        return Project.objects.get(id=project_id)
    except ObjectDoesNotExist:
        return None

