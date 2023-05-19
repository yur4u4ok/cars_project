from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.auth.views import RegisterView, TokenPairView

urlpatterns = [
    path('', TokenPairView.as_view(), name='token_obtain_pair'),
    path('/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('/register', RegisterView.as_view(), name='register_user')
]
