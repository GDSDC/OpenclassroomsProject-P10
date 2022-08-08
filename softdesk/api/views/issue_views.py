from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api.serializers import IssueSerializer
from core.issues.models import Issue
from api.views.validation_functions import get_project_and_ensure_access, not_contributor


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

        # TODO : handle case assignee_user do not exists or do not is contributor

        issue_data = request.data
        serializer = self.serializer_class(data=issue_data, context={'request': request, 'project_id': project_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # TODO : fix issue assignee_user = None -> not found
        return JsonResponse(issue_data, safe=False, status=status.HTTP_201_CREATED)
