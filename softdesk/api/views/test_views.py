from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class TestAuth(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Authenticated!',
                   'user': f'{request.user}'}
        return Response(content)
