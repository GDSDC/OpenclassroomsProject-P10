from typing import Tuple, Optional
from rest_framework import status
from core.users.models import User, Contributor
from core.projects.models import Project
from core.projects.services import project_exists, is_project_author, is_project_contributor
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

def get_project(project_id: int, author: Optional[User] = None, contributor: Optional[User] = None) \
        -> Tuple[Optional[Project], Optional[str], Optional[int]]:
    """Function to get project if it exists and Optional[if user is the author or user is contributor]"""

    if not project_exists(project_id=project_id):
        result = (None,
                  RESPONSES['project_not_found']['message'],
                  RESPONSES['project_not_found']['status'])
    else:
        project = Project.objects.get(id=project_id)
        result = (project, None, None)

        if author is not None:
            if not project.is_author(author):
                result = (None,
                          RESPONSES['not_project_author']['message'],
                          RESPONSES['not_project_author']['status'])

        if contributor is not None:
            if not is_project_contributor(project_id=project_id, contributor=contributor):
                result = (None,
                          RESPONSES['not_contributor']['message'],
                          RESPONSES['not_contributor']['status'])

    return result

# ----------- CHECK IF USER ALREADY CONTRIBUTOR OF PROJECT ------------------

def not_contributor(project_id: int, user_id: int) -> Tuple[Optional[Project], Optional[str], Optional[int]]:
    """Function to know if a user is contributor of a project"""

    user = User.objects.get(id=user_id)
    project = Project.objects.get(id=project_id)
    if is_project_contributor(project_id=project_id, contributor=user):
        result = (None,
                  RESPONSES['contributor_already_exists']['message'],
                  RESPONSES['contributor_already_exists']['status'])
    else:
        result = (user,
                  RESPONSES['not_contributor']['message'],
                  RESPONSES['not_contributor']['status'])

    return result
