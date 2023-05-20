from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.auth.serializers import TokenPairSerializer
from apps.auth.swagger.decorators import auth_register_swagger, token_pair_swagger
from apps.users.serializers import UserSerializer


@token_pair_swagger()
class TokenPairView(TokenObtainPairView):
    """
    Login
    """
    serializer_class = TokenPairSerializer


@auth_register_swagger()
class RegisterView(CreateAPIView):
    """
    Register
    """
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
