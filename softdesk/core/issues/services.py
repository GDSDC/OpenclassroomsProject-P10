from typing import Optional
from core.users.models import User
from core.issues.models import Issue
from core.projects.models import Project
from django.core.exceptions import ObjectDoesNotExist


# ----------- GETTING ISSUE BY ID ------------------

def get_issue(issue_id: int) -> Optional[Issue]:
    """Function that check if the issue exists in database"""
    try:
        return Issue.objects.get(id=issue_id)
    except ObjectDoesNotExist:
        return None

def is_issue(project:Project,issue:Issue) -> bool:
    """Function that check if an issue belongs to a project"""

    return issue in Issue.objects.filter(project=project)

