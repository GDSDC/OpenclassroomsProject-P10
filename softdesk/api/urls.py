from django.urls import path
from api.views import SignUpAPIView, TestAuth, CreateProject
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('signup/', SignUpAPIView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('projects/', CreateProject.as_view(),name='create_project'),
    # test
    path('me/', TestAuth.as_view(), name='me'),

]
