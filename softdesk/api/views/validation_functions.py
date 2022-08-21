from typing import Tuple, Optional
from rest_framework import status
from core.contributors.models import Contributor
from core.users.models import User
from core.projects.models import Project
from core.issues.models import Issue
from core.comments.models import Comment
from core.contributors import services as contributor_service
from core.issues import services as issues_service
from core.projects import services as projects_service
from core.comments import services as comments_service
from core.users.services import user_exists

MESSAGES = {
    'project_not_found': 'PROJECT NOT FOUND. WRONG ID.',
    'user_not_found': 'USER NOT FOUND. WRONG ID.',
    'issue_not_found': 'ISSUE NOT FOUND. WRONG ID.',
    'comment_not_found': 'COMMENT NOT FOUND. WRONG ID.',
    'not_project_author': 'ACCESS FORBIDDEN. PLEASE CONTACT PROJECT AUTHOR.',
    'not_project_contributor': 'ACCESS FORBIDDEN. USER IS NOT CONTRIBUTOR OF THIS PROJECT.',
    'not_issue_author': 'ACCESS FORBIDDEN. USER IS NOT AUTHOR OF THIS ISSUE.',
    'not_comment_author': 'ACCESS FORBIDDEN. USER IS NOT AUTHOR OF THIS COMMENT.',
    'contributor_already_exists': 'USER IS ALREADY CONTRIBUTOR OF THIS PROJECT.',
}


# ----------- GETTING USER BY ID ------------------

def get_user(user_id: int) -> Tuple[Optional[User], Optional[str], Optional[int]]:
    """Function to get a user if it exists"""

    if not user_exists(user_id=user_id):
        return None, MESSAGES['user_not_found'], status.HTTP_404_NOT_FOUND

    user = User.objects.get(id=user_id)
    return user, None, None


# ----------- GETTING PROJECT BY ID ------------------

def get_project_and_ensure_access(project_id: int, author: Optional[User] = None, contributor: Optional[User] = None) \
        -> Tuple[Optional[Project], Optional[str], Optional[int]]:
    """Function to get project if it exists and Optional[if user is the author or user is contributor]"""
    user = author or contributor
    if user is None:
        raise ValueError('You must pass at least one user')

    project = projects_service.get_project(project_id)
    if project is None:
        return None, MESSAGES['project_not_found'], status.HTTP_404_NOT_FOUND

    if author is not None and not contributor_service.is_contributor(project, contributor=user,
                                                                     with_role=Contributor.Role.AUTHOR):
        return project, MESSAGES['not_project_author'], status.HTTP_403_FORBIDDEN
    elif contributor is not None and not contributor_service.is_contributor(project, contributor=user):
        return project, MESSAGES['not_project_contributor'], status.HTTP_403_FORBIDDEN

    return project, None, None


# ----------- GETTING ISSUE BY ID ------------------

def get_issue_and_ensure_access(issue_id: int, author: Optional[User] = None) \
        -> Tuple[Optional[Issue], Optional[str], Optional[int]]:
    """Function to get project if it exists and Optional[if user is the author or user is contributor]"""

    issue = issues_service.get_issue(issue_id)
    if issue is None:
        return None, MESSAGES['issue_not_found'], status.HTTP_404_NOT_FOUND

    if author and not issue.author_user == author:
        return issue, MESSAGES['not_issue_author'], status.HTTP_403_FORBIDDEN

    return issue, None, None


# ----------- GETTING COMMENT BY ID ------------------

def get_comment_and_ensure_access(comment_id: int, author: Optional[User] = None) \
        -> Tuple[Optional[Comment], Optional[str], Optional[int]]:
    """Function to get project if it exists and Optional[if user is the author or user is contributor]"""

    comment = comments_service.get_comment(comment_id)
    if comment is None:
        return None, MESSAGES['comment_not_found'], status.HTTP_404_NOT_FOUND

    if author and not comment.author_user == author:
        return comment, MESSAGES['not_comment_author'], status.HTTP_403_FORBIDDEN

    return comment, None, None
