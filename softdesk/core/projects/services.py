from typing import Tuple, Optional
from core.users.models import User, Contributor
from core.projects.models import Project
from rest_framework import status

RESPONSES = {'project_not_found': {'message': 'PROJECT NOT FOUND. WRONG ID.',
                                   'status': status.HTTP_404_NOT_FOUND},
             'not_project_author': {'message': 'ACCESS FORBIDDEN. PLEASE CONTACT PROJECT AUTHOR.',
                                    'status': status.HTTP_403_FORBIDDEN},
             'user_not_found': {'message': 'USER NOT FOUND. WRONG ID.',
                                'status': status.HTTP_404_NOT_FOUND},
             'contributor_already_exists': {'message': 'USER IS ALREADY CONTRIBUTOR OF THIS PROJECT',
                                            'status': status.HTTP_400_BAD_REQUEST},
             'not_contributor': {'message': 'USER IS NOT CONTRIBUTOR OF THIS PROJECT',
                                            'status': status.HTTP_404_NOT_FOUND}
             }


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


def get_project(project_id: int, author: Optional[User] = None) \
        -> Tuple[Optional[Project], Optional[str], Optional[int]]:
    """Function to get project if it exists and if user is the author"""

    if not project_exists(project_id=project_id):
        result = (None,
                  RESPONSES['project_not_found']['message'],
                  RESPONSES['project_not_found']['status'])
    else:
        project = Project.objects.get(id=project_id)
        result = (project, None, None)

        if not is_project_author(project_id=project_id, author=author) and author is not None:
            result = (None,
                      RESPONSES['not_project_author']['message'],
                      RESPONSES['not_project_author']['status'])

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


# ----------- CHECK IF USER ALREADY CONTRIBUTOR OF PROJECT ------------------

def is_not_contributor(project_id: int, user_id: int) -> Tuple[Optional[Project], Optional[str], Optional[int]]:
    """Function to know if a user is contributor of a project"""

    user = User.objects.get(id=user_id)
    project = Project.objects.get(id=project_id)
    if Contributor.objects.filter(user_id=user, project_id=project).exists():
        result = (None,
                  RESPONSES['contributor_already_exists']['message'],
                  RESPONSES['contributor_already_exists']['status'])
    else:
        result = (user,
                  RESPONSES['not_contributor']['message'],
                  RESPONSES['not_contributor']['status'])

    return result
