from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api.serializers import IssueSerializer
from core.issues.models import Issue
from api.views.validation_functions import get_project

class Issues(APIView):
    """API View for getting infos, creating, updating or deleting an issue of a project."""
    permission_classes = [IsAuthenticated]
    serializer_class = IssueSerializer

    def get(self, request, project_id):
        """Get Issues list of project by project_id"""
        user = request.user
        project, p_message, p_status_code = get_project(project_id=project_id, contributor=user)
        if project is None:
            message = p_message
            status_code = p_status_code
        else:
            project_issues = Issue.objects.filter(project_id=project)
            issues = self.serializer_class(project_issues, many=True)
            message = issues.data
            status_code = status.HTTP_200_OK

        return JsonResponse(message,safe=False, status=status_code)