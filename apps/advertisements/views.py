from rest_framework.generics import ListAPIView, GenericAPIView, \
    DestroyAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from core.permissions.is_manager import IsManager
from .models import AdvertisementModel
from .serializers import AdvertisementSerializer
from core.check_for_bad_words.bad_words_in_description import check_for_bad_words


class ListAllAdvertsView(ListAPIView):
    queryset = AdvertisementModel.objects.filter(is_active=True)
    serializer_class = AdvertisementSerializer
    permission_classes = (AllowAny,)


class GetAdvertView(RetrieveAPIView):
    queryset = AdvertisementModel.objects.filter(is_active=True)
    serializer_class = AdvertisementSerializer
    permission_classes = (AllowAny,)


class ListCreateAdvertsView(ListCreateAPIView):
    def get_queryset(self):
        return AdvertisementModel.objects.filter(user=self.request.user)

    serializer_class = AdvertisementSerializer

    def post(self, *args, **kwargs):
        data = self.request.data

        if not self.request.user.premium and (len(self.get_queryset()) > 0):
            return Response("You should have a premium account to post more than 1 ad")

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        if check_for_bad_words(data):
            serializer.validated_data['warnings'] = 1
            serializer.save(user=self.request.user, is_active=False)
            return Response(f"Description cant contain bad words! To active your ad - edit this in your ads",
                            status.HTTP_201_CREATED)

        serializer.save(user=self.request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ACTIVATE OR UPDATE ADVERT
class ActivateUpdateAdvertView(GenericAPIView):
    def get_queryset(self):
        return AdvertisementModel.objects.filter(user=self.request.user)

    def patch(self, *args, **kwargs):
        advert = self.get_object()
        data = self.request.data

        if advert.warnings > 0 and advert.warnings % 3 == 0:
            return Response("This ad can no longer be edited...Wait for the manager verdict!",
                            status.HTTP_400_BAD_REQUEST)

        serializer = AdvertisementSerializer(advert, data, partial=True)
        serializer.is_valid(raise_exception=True)

        if data:
            if check_for_bad_words(data):
                advert.warnings += 1

                if advert.warnings % 3 == 0:
                    serializer.save(is_active=False)
                    return Response("This ad can no longer be edited...Wait for the manager verdict!",
                                    status.HTTP_400_BAD_REQUEST)

                serializer.save()
                return Response(f"Description cant contain bad words! To active your ad - edit this in your ads",
                                status.HTTP_400_BAD_REQUEST)
        else:
            if check_for_bad_words(advert.description):
                advert.warnings += 1

                if advert.warnings % 3 == 0:
                    serializer.save(is_active=False)
                    return Response("This ad can no longer be edited...Wait for the manager verdict!",
                                    status.HTTP_400_BAD_REQUEST)

                serializer.save()
                return Response(f"Description cant contain bad words! To active your ad - edit this in your ads",
                                status.HTTP_400_BAD_REQUEST)

        serializer.save(is_active=True)
        return Response(serializer.data, status.HTTP_200_OK)


class DeactivateAdvertView(GenericAPIView):
    def get_queryset(self):
        return AdvertisementModel.objects.filter(user=self.request.user)

    def patch(self, *args, **kwargs):
        advert = self.get_object()
        advert.is_active = False
        advert.save()

        serializer = AdvertisementSerializer(advert)
        return Response(serializer.data, status.HTTP_200_OK)


# FOR MANAGER
class ListSuspiciousAdvertsView(ListAPIView):
    queryset = AdvertisementModel.objects.filter(warnings__in=[num for num in range(31) if num % 3 == 0])
    serializer_class = AdvertisementSerializer
    permission_classes = (IsManager,)


# FOR MANAGER
class ApproveSuspiciousAdvertsView(GenericAPIView):
    queryset = AdvertisementModel.objects.filter(warnings__in=[num for num in range(31) if num % 3 == 0])
    serializer_class = AdvertisementSerializer
    permission_classes = (IsManager,)

    def patch(self, *args, **kwargs):
        advert = self.get_object()

        if advert.is_active:
            return Response("Already activated", status.HTTP_400_BAD_REQUEST)

        advert.is_active = True
        advert.save()

        serializer = self.get_serializer(advert)
        return Response(serializer.data, status.HTTP_200_OK)


# FOR MANAGER
class DestroyInvalidAdvertView(DestroyAPIView):
    queryset = AdvertisementModel.objects.filter(is_active=False)
    serializer_class = AdvertisementSerializer
    permission_classes = (IsManager,)
