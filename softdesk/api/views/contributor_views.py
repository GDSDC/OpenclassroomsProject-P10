from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api.serializers import UserSerializer
from core.users.models import User, Contributor
from api.views.validation_functions import get_project, not_contributor, get_user


class Contributors(APIView):
    """API View for getting infos, adding or deleting contributor of a project """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, project_id):
        """Get Contributors list of project by project_id"""
        user = request.user
        project, message, status_code = get_project(project_id=project_id)
        if project is None:
            message = message
            status_code = status_code
        else:
            project_contributors = User.objects.filter(
                id__in=[contributor.user_id.id for contributor in Contributor.objects.filter(project_id=project_id)])

            contributors = self.serializer_class(project_contributors, many=True)
            message = contributors.data
            status_code = status.HTTP_200_OK

        return JsonResponse(message, safe=False, status=status_code)

    def post(self, request, project_id, user_id):
        """Let the author of a project add a user as contributor by project_id and user_id"""
        user = request.user
        user_to_add, u_message, u_status_code = get_user(user_id=user_id)
        project, p_message, p_status_code = get_project(project_id=project_id, author=user)
        if project is None:
            message = p_message
            status_code = p_status_code
        elif user_to_add is None:
            message = u_message
            status_code = u_status_code
        else:
            c_user, c_message, c_status_code = not_contributor(project_id=project_id, user_id=user_id)
            if c_user:
                Contributor.objects.create(user_id=c_user, project_id=project, role='C')
                message = f"USER {c_user.email} ADDED TO CONTRIBUTORS OF PROJECT !"
                status_code = status.HTTP_201_CREATED
            else:
                message = c_message
                status_code = c_status_code

        return Response(message, status=status_code)

    def delete(self, request, project_id, user_id):
        """Let the author of a project delete a contributor by project_id and user_id"""
        user = request.user
        user_to_delete, u_message, u_status_code = get_user(user_id=user_id)
        project, p_message, p_status_code = get_project(project_id=project_id, author=user)
        if project is None:
            message = p_message
            status_code = p_status_code
        elif user_to_delete is None:
            message = u_message
            status_code = u_status_code
        else:
            c_user, c_message, c_status_code = not_contributor(project_id=project_id, user_id=user_id)
            if c_user:
                message = c_message
                status_code = c_status_code
            else:
                # TODO : Gérer le cas ou l'author voudrait se retirer lui-même de la liste des contributors ?
                contributor_to_remove = Contributor.objects.get(user_id=user_to_delete, project_id=project)
                contributor_to_remove.delete()
                message = f"USER {user_to_delete.email} REMOVED FROM CONTRIBUTORS OF PROJECT !"
                status_code = status.HTTP_200_OK

        return Response(message, status=status_code)
