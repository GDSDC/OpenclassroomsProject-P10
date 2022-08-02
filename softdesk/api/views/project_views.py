from rest_framework.views import APIView
from rest_framework.response import Response
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
        user_projects = Project.objects.filter(author_user_id=user)
        projects = self.serializer_class(user_projects, many=True)
        return JsonResponse(projects.data, safe=False, status=status.HTTP_200_OK)

    def post(self, request):
        """Create new Project"""
        project_data = request.data
        serializer = self.serializer_class(data=project_data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class Projects(APIView):
    """API View for getting infos, updating infos of a single project and deleting it"""
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer

    def get(self, request, project_id):
        """Get project info by project_id"""
        user = request.user
        project = Project.objects.get(author_user_id=user, id=project_id)
        result = self.serializer_class(project)
        return JsonResponse(result.data, safe=False, status=status.HTTP_200_OK)

    def put(self, request, project_id):
        """Update a project by project_id"""
        user = request.user
        project_updated_data = request.data
        project_to_update, message, status_code = get_project(project_id=project_id, author=user)
        if project_to_update is None:
            message = message
            status_code = status_code
        else:
            serializer = self.serializer_class(project_to_update, data=project_updated_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            message = serializer.data
            status_code = status.HTTP_200_OK
        return Response(message, status=status_code)

    def delete(self, request, project_id):
        """Delete project by project_id"""
        user = request.user
        project_to_delete, message, status_code = get_project(project_id=project_id, author=user)
        if project_to_delete is None:
            message = message
            status_code = status_code
        else:
            project_to_delete.delete()
            message = f"PROJECT '{project_id}' DELETED !"
            status_code = status.HTTP_200_OK
        return Response(message, status=status_code)
