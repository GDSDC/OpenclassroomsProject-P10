from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api.serializers import IssueSerializer
from core.issues.models import Issue
from api.views.validation_functions import get_project_and_ensure_access, get_issue_and_ensure_access
from core.issues import services as issue_services


class Issues(APIView):
    """API View for getting infos, creating, updating or deleting an issue of a project."""
    permission_classes = [IsAuthenticated]
    serializer_class = IssueSerializer

    def get(self, request, project_id):
        """Get Issues list of project by project_id"""

        user = request.user
        project, error_message, error_code = get_project_and_ensure_access(project_id=project_id, contributor=user)

        # error case
        if error_code is not None:
            return JsonResponse(error_message, safe=False, status=error_code)

        # get issues
        project_issues = Issue.objects.filter(project=project)
        issues = self.serializer_class(project_issues, many=True)
        message = issues.data
        return JsonResponse(message, safe=False, status=status.HTTP_200_OK)

    def post(self, request, project_id):
        """Create new Issue"""

        user = request.user
        project, error_message, error_code = get_project_and_ensure_access(project_id=project_id, contributor=user)

        # project error case
        if error_code is not None:
            return JsonResponse(error_message, safe=False, status=error_code)

        issue_data = request.data
        serializer = self.serializer_class(data=issue_data, context={'request': request, 'project_id': project_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_201_CREATED)

    def put(self, request, project_id, issue_id):
        """Update issue by issue_id of a projet by project_id"""

        user = request.user
        issue_updated_data = request.data

        # project error case
        project, error_message, error_code = get_project_and_ensure_access(project_id=project_id,
                                                                                     contributor=user)
        if error_message:
            return JsonResponse(error_message, safe=False, status=error_code)

        issue_to_update, error_message, error_code = get_issue_and_ensure_access(issue_id=issue_id, author=user)
        # issue error case
        if error_message:
            return JsonResponse(error_message, safe=False, status=error_code)

        # issue belongs to project
        if not issue_services.is_issue(project=project,issue=issue_to_update):
            return JsonResponse(f"ISSUE '{issue_to_update.id}' DO NOT BELONGS TO PROJECT '{project.id}' !")

        # update issue data
        serializer = self.serializer_class(issue_to_update, data=issue_updated_data, context={'project_id': project_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, project_id, issue_id):
        """Delete issue by issue_id of a projet by project_id"""

        user = request.user

        # project error case
        project, error_message, error_code = get_project_and_ensure_access(project_id=project_id, contributor=user)
        if error_message:
            return JsonResponse(error_message, safe=False, status=error_code)

        # issue error case
        issue_to_delete, error_message, error_code = get_issue_and_ensure_access(issue_id=issue_id, author=user)
        if error_message:
            return JsonResponse(error_message, safe=False, status=error_code)

        # issue belongs to project
        if not issue_services.is_issue(project=project,issue=issue_to_delete):
            return JsonResponse(f"ISSUE '{issue_to_delete.id}' DO NOT BELONGS TO PROJECT '{project.id}' !")

        # delete issue
        issue_to_delete.delete()
        return JsonResponse(f"ISSUE '{issue_id}' DELETED !", safe=False, status=status.HTTP_200_OK)
