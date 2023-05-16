from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status

from apps.users.models import UserModel
from apps.users.serializers import UserSerializer
from core.permissions.is_superuser import IsSuperUser
from core.permissions.is_manager import IsManager


# FOR MANAGER
class GetAllUsersView(ListAPIView):
    queryset = UserModel.objects.filter(is_staff=False)
    serializer_class = UserSerializer
    permission_classes = (IsManager,)


# FOR MANAGER
class UserBlockView(GenericAPIView):
    permission_classes = (IsManager,)
    queryset = UserModel.objects.filter(is_staff=False)

    def patch(self, *args, **kwargs):
        user = self.get_object()

        if not user.is_active:
            return Response("You cant do that", status=status.HTTP_400_BAD_REQUEST)

        user.is_active = False
        user.save()
        serializer = UserSerializer(user)

        return Response(serializer.data, status.HTTP_200_OK)


# FOR MANAGER
class UserUnBlockView(GenericAPIView):
    permission_classes = (IsManager,)
    queryset = UserModel.objects.filter(is_staff=False)

    def patch(self, *args, **kwargs):
        user = self.get_object()

        if user.is_active:
            return Response("You cant do that", status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save()
        serializer = UserSerializer(user)

        return Response(serializer.data, status.HTTP_200_OK)


# FOR SUPERUSER
class UserToManagerView(GenericAPIView):
    permission_classes = (IsSuperUser,)

    def get_queryset(self):
        return UserModel.objects.exclude(pk=self.request.user.pk)

    def patch(self, *args, **kwargs):
        user = self.get_object()

        if user.is_staff or not user.is_active:
            return Response("You cant do that with this user", status=status.HTTP_400_BAD_REQUEST)

        user.is_staff = True
        user.premium = True
        user.save()
        serializer = UserSerializer(user)

        return Response(serializer.data, status.HTTP_200_OK)


# FOR SUPERUSER
class ManagerToUserView(GenericAPIView):
    permission_classes = (IsSuperUser,)

    def get_queryset(self):
        return UserModel.objects.exclude(pk=self.request.user.pk)

    def patch(self, *args, **kwargs):
        user = self.get_object()

        if not user.is_staff or not user.is_active or user.is_superuser:
            return Response("You cant do that with this user", status=status.HTTP_400_BAD_REQUEST)

        user.is_staff = False
        user.premium = False
        user.save()
        serializer = UserSerializer(user)

        return Response(serializer.data, status.HTTP_200_OK)


# FOR SUPERUSER
class ManagerBlockView(GenericAPIView):
    permission_classes = (IsSuperUser,)

    def get_queryset(self):
        return UserModel.objects.filter(is_staff=True).exclude(pk=self.request.user.pk)

    def patch(self, *args, **kwargs):
        user = self.get_object()

        if user.is_superuser or not user.is_active:
            return Response("You cant do that with this user", status.HTTP_400_BAD_REQUEST)

        user.is_active = False
        user.save()
        serializer = UserSerializer(user)

        return Response(serializer.data, status.HTTP_200_OK)


# FOR SUPERUSER
class ManagerUnBlockView(GenericAPIView):
    permission_classes = (IsSuperUser,)

    def get_queryset(self):
        return UserModel.objects.filter(is_staff=True).exclude(pk=self.request.user.pk)

    def patch(self, *args, **kwargs):
        user = self.get_object()

        if user.is_active:
            return Response("You cant do that with this user", status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save()
        serializer = UserSerializer(user)

        return Response(serializer.data, status.HTTP_200_OK)
