from django.urls import path
from api.views.user_views import SignUpAPIView
from api.views.test_views import TestAuth
from api.views.project_views import GeneralProjects, Projects
from api.views.contributor_views import Contributors
from api.views.issue_views import Issues
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('signup/', SignUpAPIView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('projects/', GeneralProjects.as_view()),
    path('projects/<int:project_id>/', Projects.as_view()),
    path('projects/<int:project_id>/users/', Contributors.as_view()),
    path('projects/<int:project_id>/users/<int:user_id>', Contributors.as_view()),
    path('projects/<int:project_id>/issues/', Issues.as_view()),
    path('projects/<int:project_id>/issues/<int:issue_id>', Issues.as_view()),

    # test
    path('me/', TestAuth.as_view(), name='me'),

]
