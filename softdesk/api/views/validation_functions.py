from typing import Tuple, Optional
from rest_framework import status
from core.contributors.models import Contributor
from core.users.models import User
from core.projects.models import Project
from core.issues.models import Issue
from core.contributors import services as contributor_service
from core.issues import services as issues_service
from core.projects import services as project_service
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
                                 'status': status.HTTP_403_FORBIDDEN},
             'issue_not_found': {'message': 'ISSUE NOT FOUND. WRONG ID.',
                                 'status': status.HTTP_404_NOT_FOUND},
             'not_issue_author': {'message': 'USER IS NOT AUTHOR OF THIS ISSUE',
                                  'status': status.HTTP_403_FORBIDDEN},
             }


# ----------- GETTING USER BY ID ------------------

def get_user(user_id: int) -> Tuple[Optional[User], Optional[str], Optional[int]]:
    """Function to get a user if it exists"""

    if not user_exists(user_id=user_id):
        return None, RESPONSES['user_not_found']['message'], RESPONSES['user_not_found']['status']

    user = User.objects.get(id=user_id)
    return user, None, None


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

    role = Contributor.Role.AUTHOR if author is not None else None
    if not contributor_service.is_contributor(project, contributor=user, with_role=role):
        return project, RESPONSES['not_contributor']['message'], status.HTTP_403_FORBIDDEN

    return project, None, None


# ----------- GETTING ISSUE BY ID ------------------

def get_issue_and_ensure_access(issue_id: int, author: User) \
        -> Tuple[Optional[Issue], Optional[str], Optional[int]]:
    """Function to get project if it exists and Optional[if user is the author or user is contributor]"""
    user = author
    if user is None:
        raise ValueError('You must pass at least one user')

    issue = issues_service.get_issue(issue_id)
    if issue is None:
        return None, RESPONSES['issue_not_found']['message'], status.HTTP_404_NOT_FOUND

    if not issue.author_user == user:
        return issue, RESPONSES['not_issue_author']['message'], status.HTTP_403_FORBIDDEN

    return issue, None, None
