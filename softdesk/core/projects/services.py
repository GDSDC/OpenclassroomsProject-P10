from typing import Tuple, Optional
from core.users.models import User
from core.projects.models import Project
from rest_framework import status

RESPONSES = {'project_not_found': {'message': 'PROJECT NOT FOUND. WRONG ID.',
                                   'status': status.HTTP_404_NOT_FOUND},
             'not_project_author': {'message': 'ACCESS FORBIDDEN. PLEASE CONTACT PROJECT AUTHOR.',
                                    'status': status.HTTP_403_FORBIDDEN},
             'user_not_found': {'message': 'USER NOT FOUND. WRONG ID.',
                                'status': status.HTTP_404_NOT_FOUND}
             }


# ----------- GETTING PROJECT BY ID ------------------

def project_exists(project_id: int) -> bool:
    """Function that check if the project exists in database"""

    return Project.objects.filter(id=project_id).exists()


def is_project_author(project_id: int, user: User) -> bool:
    """Function that check if the user is the author of the poject"""

    project = Project.objects.get(id=project_id)
    if project.author_user_id == user:
        return True
    else:
        return False


def get_project(project_id: int, user: User) -> Tuple[Optional[Project], Optional[str], Optional[int]]:
    """Function to get project if it exists and if user is the author"""

    if not project_exists(project_id=project_id):
        result = (None,
                  RESPONSES['project_not_found']['message'],
                  RESPONSES['project_not_found']['status'])
    elif not is_project_author(project_id=project_id, user=user):
        result = (None,
                  RESPONSES['not_project_author']['message'],
                  RESPONSES['not_project_author']['status'])
    else:
        project = Project.objects.get(id=project_id)
        result = (project, None, None)

    return result


# ----------- GETTING USER BY ID ------------------

def user_exists(user_id: int) -> bool:
    """Function that check if users exists in database"""

    return User.objects.filter(id=user_id).exists()


def get_user(user_id: int) -> Tuple[Optional[Project], Optional[str], Optional[int]]:
    """Function to get a user if it exists"""

    if not user_exists(user_id=user_id):
        result = (None,
                  RESPONSES['user_not_found']['message'],
                  RESPONSES['user_not_found']['status'])
    else:
        user = User.objects.get(id=user_id)
        result = (user, None, None)

    return result
