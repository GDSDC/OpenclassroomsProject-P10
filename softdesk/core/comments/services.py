from typing import Optional
from core.comments.models import Comment
from django.core.exceptions import ObjectDoesNotExist


# ----------- GETTING COMMENT BY ID ------------------

def get_comment(comment_id: int) -> Optional[Comment]:
    """Function that check if the comment exists in database"""
    try:
        return Comment.objects.get(id=comment_id)
    except ObjectDoesNotExist:
        return None



