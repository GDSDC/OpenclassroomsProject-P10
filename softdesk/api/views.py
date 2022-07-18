from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.permissions import IsOwner
from api.serializers import UserSignUpSerializer, ProjectSerializer
from django.contrib.auth import authenticate, login
from core.users.models import User
from core.projects.models import Project
import json
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, permission_classes


class SignUpAPIView(APIView):
    """API class view for signing up"""

    # Allow any user (authenticated or not) to access this url
    permission_classes = (AllowAny,)
    serializer_class = UserSignUpSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TestAuth(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Authenticated!',
                   'user': f'{request.user}'}
        return Response(content)


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
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = ProjectSerializer

    def get(self, request, project_id):
        """Get project info by project_id"""
        user = request.user
        project = Project.objects.get(author_user_id=user, id=project_id)
        result = self.serializer_class(project)
        return JsonResponse(result.data, safe=False, status=status.HTTP_200_OK)

    def put(self, request, project_id):
        """Update a project by project_id"""
        project_updated_data = request.data
        project_to_update = Project.objects.get(id=project_id)
        serializer = self.serializer_class(project_to_update, data=project_updated_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, project_id):
        """Delete project by project_id"""
        user = request.user
        project_to_delete = Project.objects.get(author_user_id=user, id=project_id)
        project_to_delete.delete()
        return Response(f"Project '{project_id}' deleted !", status=status.HTTP_200_OK)
