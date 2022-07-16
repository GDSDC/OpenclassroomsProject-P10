from django.urls import path
from api.views import SignUpAPIView, TestAuth, Projects
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('signup/', SignUpAPIView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('projects/', Projects.as_view()),
    # TODO : work on two path lines for same root but one for post and other for get
    #  the idea is to make separate class APIView with better naming

    # test
    path('me/', TestAuth.as_view(), name='me'),

]
