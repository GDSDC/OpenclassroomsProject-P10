from core.projects.models import Project
from core.users.models import User, Contributor


# ----------- GETTING PROJECT BY ID ------------------

def project_exists(project_id: int) -> bool:
    """Function that check if the project exists in database"""

    return Project.objects.filter(id=project_id).exists()


def is_project_author(project_id: int, author: User) -> bool:
    """Function that check if the user is the author of the poject"""

    project = Project.objects.get(id=project_id)
    if project.author_user_id == author:
        return True
    else:
        return False


def is_project_contributor(project_id: int, contributor: User) -> bool:
    """Function that check if the user is a contributor of the poject"""

    project = Project.objects.get(id=project_id)
    return Contributor.objects.filter(project_id=project, user_id=contributor).exists()
