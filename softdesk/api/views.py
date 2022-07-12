from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from api.serializers import SignUpSerializer
from django.contrib.auth import authenticate, login


class SignUpAPIView(APIView):
    """API class view for signing up"""

    # Allow any user (authenticated or not) to access this url
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        serializer = SignUpSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def post(self, request):
    #     data = dict(request.POST.items())
    #     try:
    #         email = data['email']
    #         password1 = data['password1']
    #         password2 = data['password2']
    #         first_name = data['first_name']
    #         last_name = data['last_name']
    #
    #         try:
    #             validate_email(email)
    #             if User.objects.filter(email=email).exists():
    #                 return Response('EMAIL ALREADY EXISTS', status=status.HTTP_409_CONFLICT)
    #
    #             else:
    #                 if password1 != password2:
    #                     return Response('DIFFERENT PASSWORDS !', status=status.HTTP_400_BAD_REQUEST)
    #                 else:
    #                     new_user = User()
    #                     new_user.email = email
    #                     new_user.first_name = first_name
    #                     new_user.last_name = last_name
    #                     new_user.password = password1
    #                     new_user.save()
    #                     return Response(f'New user {email} created in database !', status=status.HTTP_201_CREATED)
    #         except ValidationError:
    #             return Response('INVALID EMAIL', status=status.HTTP_400_BAD_REQUEST)
    #
    #
    #     except KeyError:
    #         return Response('WRONG DATA FORMAT. Please enter email, first_name, last_name, and password.',
    #                         status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    """API class view for login in"""

    def post(self, request):
        data = dict(request.POST.items())
        try:
            user_email = data['email']
            user_password = data['password']

            user = authenticate(email=user_email, password=user_password)
            if user is not None and user.is_active:
                login(request, user)
                return Response(f'User {user_email} logged in successfully')
            else:
                return Response('INVAVID LOGIN CREDENTIALS', status=status.HTTP_401_UNAUTHORIZED)



        except KeyError:
            return Response('WRONG DATA FORMAT. Please enter email and password.', status=status.HTTP_400_BAD_REQUEST)
