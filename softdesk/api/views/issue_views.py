from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api.serializers import IssueSerializer
from core.issues.models import Issue
from api.views.validation_functions import get_project_and_ensure_access, get_issue_and_ensure_access


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
        return JsonResponse(issue_data, safe=False, status=status.HTTP_201_CREATED)

    def put(self, request, project_id, issue_id):
        """Update issue by issue_id of a projet by project_id"""

        # TODO : s'assurer que cela marche
        #  travailler sur get_issue_and_ensure_access pour s'assurer que celui qui modifie/supprime est bien l'auteur
        user = request.user
        issue_updated_data = request.data
        project_to_update, error_message, error_code = get_project_and_ensure_access(project_id=project_id, contributor=user)

        # project error case
        if error_message:
            return JsonResponse(error_message, safe=False, status=error_code)

        issue_to_update, error_message, error_code = get_issue_and_ensure_access(issue_id=issue_id, author=user)
        # issue error case
        if error_message:
            return JsonResponse(error_message, safe=False, status=error_code)

        # update issue data
        serializer = self.serializer_class(issue_to_update, data=issue_updated_data, context={'project_id': project_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
