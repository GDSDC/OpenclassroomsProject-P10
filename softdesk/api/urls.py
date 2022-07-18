from django.urls import path
from api.views import SignUpAPIView, TestAuth, GeneralProjects, Projects
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('signup/', SignUpAPIView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('projects/', GeneralProjects.as_view()),
    path('projects/<int:project_id>/', Projects.as_view()),


    # test
    path('me/', TestAuth.as_view(), name='me'),

]
