from core.projects.models import Project
from core.users.models import User, Contributor


# ----------- GETTING PROJECT BY ID ------------------

def project_exists(project_id: int) -> bool:
    """Function that check if the project exists in database"""

    return Project.objects.filter(id=project_id).exists()


def is_project_contributor(project: Project, contributor: User) -> bool:
    """Function that check if the user is a contributor of the poject"""

    return Contributor.objects.filter(project_id=project, user_id=contributor).exists()
