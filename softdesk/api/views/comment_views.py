from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api.serializers import CommentSerializer
from api.views.validation_functions import get_project_and_ensure_access
from core.comments.models import Comment


class GeneralComments(APIView):
    """API View for creating a comment and getting list of all comments for an issue"""
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get(self, request, project_id, issue_id):
        """Get list of comments for an issue of a project"""

        user = request.user

        # project error case
        project, error_message, error_code = get_project_and_ensure_access(project_id=project_id, contributor=user)
        if error_message:
            return JsonResponse(error_message, safe=False, status=error_code)

        # get comments
        issue_comments = Comment.objects.filter(issue_id=issue_id)
        comments = self.serializer_class(issue_comments, many=True)
        message = comments.data
        return JsonResponse(message, safe=False, status=status.HTTP_200_OK)

    def post(self, request, project_id, issue_id):
        """Create new comment for an issue of a project"""

        user = request.user

        # project error case
        project, error_message, error_code = get_project_and_ensure_access(project_id=project_id, contributor=user)
        if error_message:
            return JsonResponse(error_message, safe=False, status=error_code)

        comment_data = request.data
        serializer = self.serializer_class(data=comment_data, context={'request': request, 'issue_id': issue_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_201_CREATED)
