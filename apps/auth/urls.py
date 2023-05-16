from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.auth.views import RegisterView

urlpatterns = [
    path('', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('/register', RegisterView.as_view(), name='register_user')
]