from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api.serializers import CommentSerializer
from api.views.validation_functions import \
    get_project_and_ensure_access, \
    get_issue_and_ensure_access, \
    get_comment_and_ensure_access
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

        # issue error case
        issue, error_message, error_code = get_issue_and_ensure_access(issue_id=issue_id, project=project)
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

        # issue error case
        issue, error_message, error_code = get_issue_and_ensure_access(issue_id=issue_id, project=project)
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
        issue, error_message, error_code = get_issue_and_ensure_access(issue_id=issue_id, project=project)
        if error_message:
            return JsonResponse(error_message, safe=False, status=error_code)

        # comment error case
        comment, error_message, error_code = get_comment_and_ensure_access(comment_id=comment_id, issue=issue)
        if error_message:
            return JsonResponse(error_message, safe=False, status=error_code)

        # get comment data
        return JsonResponse(self.serializer_class(comment).data, safe=False, status=status.HTTP_200_OK)

    def put(self, request, project_id, issue_id, comment_id):
        """Update comment"""

        user = request.user
        comment_updated_data = request.data

        # project error case
        project, error_message, error_code = get_project_and_ensure_access(project_id=project_id, contributor=user)
        if error_message:
            return JsonResponse(error_message, safe=False, status=error_code)

        # issue error case
        issue, error_message, error_code = get_issue_and_ensure_access(issue_id=issue_id, project=project)
        if error_message:
            return JsonResponse(error_message, safe=False, status=error_code)

        # comment error case
        comment_to_update, error_message, error_code = get_comment_and_ensure_access(comment_id=comment_id, issue=issue,
                                                                                     author=user)
        if error_message:
            return JsonResponse(error_message, safe=False, status=error_code)

        # update comment data
        serializer = self.serializer_class(comment_to_update, data=comment_updated_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, project_id, issue_id, comment_id):
        """Delete comment"""

        user = request.user

        # project error case
        project, error_message, error_code = get_project_and_ensure_access(project_id=project_id, contributor=user)
        if error_message:
            return JsonResponse(error_message, safe=False, status=error_code)

        # issue error case
        issue, error_message, error_code = get_issue_and_ensure_access(issue_id=issue_id, project=project)
        if error_message:
            return JsonResponse(error_message, safe=False, status=error_code)

        # comment error case
        comment_to_delete, error_message, error_code = get_comment_and_ensure_access(comment_id=comment_id, issue=issue,
                                                                                     author=user)
        if error_message:
            return JsonResponse(error_message, safe=False, status=error_code)

        # delete comment
        comment_to_delete.delete()
        return JsonResponse(f"COMMENT '{comment_id}' DELETED !", safe=False, status=status.HTTP_200_OK)

