from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api.serializers import UserSerializer
from core.contributors.models import Contributor
from core.users.models import User
from api.views.validation_functions import get_project_and_ensure_access, not_contributor, get_user


class Contributors(APIView):
    """API View for getting infos, adding or deleting contributor of a project """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, project_id):
        """Get Contributors list of project by project_id"""
        user = request.user
        project, error_message, error_code = get_project_and_ensure_access(project_id=project_id, contributor=user)
        if error_code is not None:
            # error case
            return JsonResponse(error_message, safe=False, status=error_code)

        project_contributors = User.objects.filter(
            id__in=[contributor.user_id for contributor in Contributor.objects.filter(project_id=project_id)]
        )

        contributors = self.serializer_class(project_contributors, many=True)
        message = contributors.data

        return JsonResponse(message, safe=False, status=status.HTTP_200_OK)

    def post(self, request, project_id, user_id):
        """Let the author of a project add a user as contributor by project_id and user_id"""

        user = request.user

        user_to_add, error_message, error_code = get_user(user_id=user_id)
        if error_code is not None:
            # user_to_add do not exist
            return JsonResponse(error_message, safe=False, status=error_code)

        project, error_message, error_code = get_project_and_ensure_access(project_id=project_id, author=user)
        if error_code is not None:
            # error case
            return JsonResponse(error_message, safe=False, status=error_code)

        contributor_to_create, error_message, error_code = not_contributor(project=project, user=user_to_add)
        if contributor_to_create:
            Contributor.objects.create(user=contributor_to_create, project=project, role='C')
            message = f"USER {contributor_to_create.email} ADDED TO CONTRIBUTORS OF PROJECT !"
            status_code = status.HTTP_201_CREATED
        else:
            message = error_message
            status_code = error_code

        return JsonResponse(message, safe=False, status=status_code)

    def delete(self, request, project_id, user_id):
        """Let the author of a project delete a contributor by project_id and user_id"""
        user = request.user

        user_to_delete, error_message, error_code = get_user(user_id=user_id)
        if error_code is not None:
            # user_to_delete do not exist
            return JsonResponse(error_message, safe=False, status=error_code)

        project, error_message, error_code = get_project_and_ensure_access(project_id=project_id, author=user)
        if error_code is not None:
            # error case
            return JsonResponse(error_message, safe=False, status=error_code)

        contributor_to_delete, error_message, error_code = not_contributor(project=project, user=user_to_delete)
        if contributor_to_delete:
            message = error_message
            status_code = error_code
        else:
            # TODO : Gérer le cas ou l'author voudrait se retirer lui-même de la liste des contributors ?
            Contributor.objects.get(user=user_to_delete, project=project).delete()
            message = f"USER {user_to_delete.email} REMOVED FROM CONTRIBUTORS OF PROJECT !"
            status_code = status.HTTP_200_OK

        return JsonResponse(message, safe=False, status=status_code)
