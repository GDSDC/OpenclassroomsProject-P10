from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.serializers import UserSignUpSerializer, ProjectCreationSerializer
from django.contrib.auth import authenticate, login
from core.users.models import User
from core.projects.models import Project
import json
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
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Authenticated!',
                   'user': f'{request.user}'}
        return Response(content)


class Projects(APIView):
    """API View for creating a project"""
    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectCreationSerializer

    def get(self, request):
        """Get list of projects created by user"""
        user = request.user
        projects = []
        user_projects = Project.objects.filter(author_user_id=user)
        for project in user_projects:
            projects.append(self.serializer_class(project).data)
        json_data = json.dumps(projects)
        # TODO : work on proper json result
        return Response(json_data, status=status.HTTP_201_CREATED)

    def post(self, request):
        """Create new Project"""
        project_data = request.data
        serializer = self.serializer_class(data=project_data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
