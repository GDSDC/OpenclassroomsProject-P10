from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api.serializers import ProjectSerializer
from core.projects.models import Project
from api.views.validation_functions import get_project_and_ensure_access


class GeneralProjects(APIView):
    """API View for creating a project and getting list of all projects for a user"""
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer

    def get(self, request):
        """Get list of projects created by user"""
        user = request.user
        user_projects = Project.objects.filter(author_user=user)
        projects = self.serializer_class(user_projects, many=True)
        return JsonResponse(projects.data, safe=False, status=status.HTTP_200_OK)

    def post(self, request):
        """Create new Project"""
        project_data = request.data
        serializer = self.serializer_class(data=project_data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_201_CREATED)


class Projects(APIView):
    """API View for getting infos, updating infos of a single project and deleting it"""
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer

    def get(self, request, project_id):
        """Get project info by project_id"""

        user = request.user

        # project error case
        project, error_message, error_code = get_project_and_ensure_access(project_id=project_id, contributor=user)
        if error_message:
            return JsonResponse(error_message, safe=False, status=error_code)

        # get project data
        return JsonResponse(self.serializer_class(project).data, safe=False, status=status.HTTP_200_OK)

    def put(self, request, project_id):
        """Update a project by project_id"""

        user = request.user
        project_updated_data = request.data

        # project error case
        project_to_update, error_message, error_code = get_project_and_ensure_access(project_id=project_id, author=user)
        if error_message:
            return JsonResponse(error_message, safe=False, status=error_code)

        # update project data
        serializer = self.serializer_class(project_to_update, data=project_updated_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, project_id):
        """Delete project by project_id"""

        user = request.user

        # project error case
        project_to_delete, error_message, error_code = get_project_and_ensure_access(project_id=project_id, author=user)
        if error_message:
            return JsonResponse(error_message, safe=False, status=error_code)

        # delete project
        project_to_delete.delete()
        return JsonResponse(f"PROJECT '{project_id}' DELETED !", safe=False, status=status.HTTP_200_OK)
