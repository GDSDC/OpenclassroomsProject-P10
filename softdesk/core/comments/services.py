from typing import Optional

from django.core.exceptions import ObjectDoesNotExist

from core.comments.models import Comment
from core.issues.models import Issue


# ----------- GETTING COMMENT BY ID ------------------

def get_comment(comment_id: int) -> Optional[Comment]:
    """Function that check if the comment exists in database"""
    try:
        return Comment.objects.get(id=comment_id)
    except ObjectDoesNotExist:
        return None


# ----------- CHECKING IF COMMENT BELONGS TO ISSUE ------------------

def is_comment(issue: Issue, comment: Comment) -> bool:
    """Function that check if an issue belongs to a project"""

    return comment in Comment.objects.filter(issue=issue)
