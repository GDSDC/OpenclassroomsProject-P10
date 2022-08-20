from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api.serializers import ContributorSerializer
from core.contributors.models import Contributor
from core.users.models import User
from core.contributors import services as contributor_service
from api.views.validation_functions import get_project_and_ensure_access, get_user


class Contributors(APIView):
    """API View for getting infos, adding or deleting contributor of a project """
    permission_classes = [IsAuthenticated]
    serializer_class = ContributorSerializer

    def get(self, request, project_id):
        """Get Contributors list of project by project_id"""

        user = request.user
        project, error_message, error_code = get_project_and_ensure_access(project_id=project_id, contributor=user)

        # error case
        if error_code is not None:
            return JsonResponse(error_message, safe=False, status=error_code)

        # get contributors
        project_contributors = Contributor.objects.filter(
            id__in=[contributor.id for contributor in Contributor.objects.filter(project_id=project_id)])
        contributors = self.serializer_class(project_contributors, many=True)
        message = contributors.data
        return JsonResponse(message, safe=False, status=status.HTTP_200_OK)

    def post(self, request, project_id, user_id):
        """Let the author of a project add a user as contributor by project_id and user_id"""

        user = request.user
        user_to_add, error_message, error_code = get_user(user_id=user_id)

        # error case : user_to_add do not exist
        if error_code is not None:
            return JsonResponse(error_message, safe=False, status=error_code)

        project, error_message, error_code = get_project_and_ensure_access(project_id=project_id, author=user)

        # project error case
        if error_code is not None:
            return JsonResponse(error_message, safe=False, status=error_code)

        # create contributor
        is_contributor = contributor_service.is_contributor(project=project, contributor=user_to_add)
        if not is_contributor:
            Contributor.objects.create(user=user_to_add, project=project, role='CONTRIBUTOR')
            message = f"USER {user_to_add.email} ADDED TO CONTRIBUTORS OF PROJECT !"
            status_code = status.HTTP_201_CREATED
        else:
            message = f"USER {user_to_add.email} WAS ALREADY A CONTRIBUTOR !"
            status_code = status.HTTP_200_OK
        return JsonResponse(message, safe=False, status=status_code)

    def delete(self, request, project_id, user_id):
        """Let the author of a project delete a contributor by project_id and user_id"""

        user = request.user
        user_to_delete, error_message, error_code = get_user(user_id=user_id)

        # error case : user_to_delete do not exist
        if error_code is not None:
            return JsonResponse(error_message, safe=False, status=error_code)

        project, error_message, error_code = get_project_and_ensure_access(project_id=project_id, author=user)

        # project error case
        if error_code is not None:
            return JsonResponse(error_message, safe=False, status=error_code)

        # delete contributor
        # TODO : Gérer le cas ou l'author voudrait se retirer lui-même de la liste des contributors ?
        deleted_count, _ = Contributor.objects.filter(user=user_to_delete, project=project).delete()
        if deleted_count:
            message = f"USER {user_to_delete.email} REMOVED FROM CONTRIBUTORS OF PROJECT !"
            status_code = status.HTTP_200_OK
        else:
            message = f"USER {user_to_delete.email} IS NOT CONTRIBUTOR OF PROJECT !"
            status_code = status.HTTP_204_NO_CONTENT
        return JsonResponse(message, safe=False, status=status_code)
