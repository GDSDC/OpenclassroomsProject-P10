from typing import Tuple, Optional
from rest_framework import status
from core.users.models import ContributorRole, User, Contributor
from core.projects.models import Project
from core.projects import services as project_service
from core.projects.services import project_exists, is_contributor
from core.users.services import user_exists

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


# ----------- GETTING USER BY ID ------------------

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


# ----------- GETTING PROJECT BY ID ------------------

def get_project_and_ensure_access(project_id: int, author: Optional[User] = None, contributor: Optional[User] = None) \
        -> Tuple[Optional[Project], Optional[str], Optional[int]]:
    """Function to get project if it exists and Optional[if user is the author or user is contributor]"""
    user = author or contributor
    if user is None:
        raise ValueError('You must pass at least one user')

    project = project_service.get_project(project_id)
    if project is None:
        return None, RESPONSES['project_not_found']['message'], status.HTTP_404_NOT_FOUND

    role = ContributorRole.AUTHOR if author is not None else None
    if not project_service.is_contributor(project, contributor=user, with_role=role):
        return project, RESPONSES['not_contributor']['message'], status.HTTP_403_FORBIDDEN

    return project, None, None


# ----------- CHECK IF USER ALREADY CONTRIBUTOR OF PROJECT ------------------

def not_contributor(project_id: int, user_id: int) -> Tuple[Optional[Project], Optional[str], Optional[int]]:
    """Function to know if a user is contributor of a project"""

    user = User.objects.get(id=user_id)
    project = Project.objects.get(id=project_id)
    if is_contributor(project_id=project_id, contributor=user):
        result = (None,
                  RESPONSES['contributor_already_exists']['message'],
                  RESPONSES['contributor_already_exists']['status'])
    else:
        result = (user,
                  RESPONSES['not_contributor']['message'],
                  RESPONSES['not_contributor']['status'])

    return result
