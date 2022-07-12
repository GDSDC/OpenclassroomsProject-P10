from django.urls import path
from api.views import SignUpAPIView, Login

urlpatterns = [
    path('signup/', SignUpAPIView.as_view()),
    path('login/', Login.as_view()),
]
