from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api.serializers import CommentSerializer
from api.views.validation_functions import get_project_and_ensure_access, get_issue_and_ensure_access
from core.comments.models import Comment
from core.issues import services as issue_services
from core.comments import services as comment_services


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


class Comments(APIView):
    """API View for getting infos, updating infos of a single comment and deleting it"""
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get(self, request, project_id, issue_id, comment_id):
        """Get comment info by comment_id"""

        user = request.user

        # project error case
        project, error_message, error_code = get_project_and_ensure_access(project_id=project_id, contributor=user)
        if error_message:
            return JsonResponse(error_message, safe=False, status=error_code)

        # issue error case
        issue, error_message, error_code = get_issue_and_ensure_access(issue_id=issue_id)
        if error_message:
            return JsonResponse(error_message, safe=False, status=error_code)

        # issue belongs to project
        if not issue_services.is_issue(project=project,issue=issue):
            return JsonResponse(f"ISSUE '{issue.id}' DO NOT BELONGS TO PROJECT '{project.id}' !")

        # comment error case
        comment = comment_services.get_comment(comment_id=comment_id)
        if not comment:
            return JsonResponse('COMMENT NOT FOUND. WRONG ID.', safe=False, status=status.HTTP_404_NOT_FOUND)

        # get comment data
        return JsonResponse(self.serializer_class(comment).data, safe=False, status=status.HTTP_200_OK)
