from rest_framework.generics import ListAPIView, GenericAPIView, \
    DestroyAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from django.db.models import Sum
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from drf_yasg.utils import swagger_auto_schema

from math import floor

from core.permissions.is_manager import IsManager
from .models import AdvertisementModel, AdvertisementPhotoModel
from .serializers import AdvertisementSerializer, AdvertPhotoSerializer
from core.check_for_bad_words.bad_words_in_description import check_for_bad_words

from .swagger.decorators import advert_swagger
from .swagger.serializers import SwaggerAdvertSerializer


@method_decorator(swagger_auto_schema(security=[]), 'get')
class ListAllAdvertsView(ListAPIView):
    """
    Get all adverts
    """
    queryset = AdvertisementModel.objects.filter(is_active=True)
    serializer_class = AdvertisementSerializer
    permission_classes = (AllowAny,)


@method_decorator(swagger_auto_schema(security=[]), 'get')
class GetAdvertView(RetrieveAPIView):
    """
    Get advert by id
    """
    queryset = AdvertisementModel.objects.filter(is_active=True)
    serializer_class = AdvertisementSerializer
    permission_classes = (AllowAny,)

    def get(self, *args, **kwargs):
        advert = self.get_object()
        advert.views += 1
        advert.save()

        serializer = self.get_serializer(advert)

        return Response(serializer.data, status.HTTP_200_OK)


class ListCreateAdvertsView(ListCreateAPIView):
    """
    get:
        Get all adverts of registered user
    post:
        Post advert
    """

    def get_queryset(self):
        return AdvertisementModel.objects.filter(user=self.request.user)

    serializer_class = AdvertisementSerializer

    def post(self, *args, **kwargs):
        queryset = AdvertisementModel.objects.filter(user=self.request.user, is_active=True).count()
        data = self.request.data

        if not self.request.user.premium and queryset > 0:
            return Response("You should have a premium account to post more than 1 ad",
                            status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        if check_for_bad_words(data):
            serializer.validated_data['warnings'] = 1
            serializer.save(user=self.request.user, car_brand=data['car_brand'].upper(),
                            car_model=data['car_model'].upper(), city=data['city'].upper(), is_active=False)

            return Response(f"Description cant contain bad words! To active your ad - edit this in your ads",
                            status.HTTP_201_CREATED)

        serializer.save(user=self.request.user, car_brand=data['car_brand'].upper(),
                        car_model=data['car_model'].upper(), city=data['city'].upper())

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateAdvertView(GenericAPIView):
    """
    Update advert
    """
    def get_queryset(self):
        return AdvertisementModel.objects.filter(user_id=self.request.user.id)

    serializer_class = AdvertisementSerializer

    @swagger_auto_schema(responses={status.HTTP_200_OK: SwaggerAdvertSerializer()})
    def patch(self, *args, **kwargs):
        advert = self.get_object()
        data = self.request.data

        if advert.warnings > 0 and advert.warnings % 3 == 0:
            return Response("This ad can no longer be edited...Wait for the manager verdict!",
                            status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(advert, data, partial=True)
        serializer.is_valid(raise_exception=True)

        if check_for_bad_words(data):
            advert.warnings += 1

            if advert.warnings % 3 == 0:
                serializer.save(is_active=False)
                return Response("This ad can no longer be edited...Wait for the manager verdict!",
                                status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(f"Description cant contain bad words!",
                            status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)


class DeleteAdvertView(DestroyAPIView):
    """
    Delete advert
    """

    def get_queryset(self):
        return AdvertisementModel.objects.filter(user_id=self.request.user.id)

    serializer_class = AdvertisementSerializer


class AdvertAddPhotoView(GenericAPIView):
    """
    Post photo to advert
    """
    serializer_class = AdvertPhotoSerializer

    def get_queryset(self):
        return AdvertisementModel.objects.filter(user_id=self.request.user.id)

    @swagger_auto_schema(responses={status.HTTP_201_CREATED: SwaggerAdvertSerializer()})
    def post(self, *args, **kwargs):
        files = self.request.FILES
        advert = self.get_object()
        for key in files:
            serializer = self.get_serializer(data={'photo': files[key]})
            serializer.is_valid(raise_exception=True)
            serializer.save(advert=advert)
        serializer = AdvertisementSerializer(advert)
        return Response(serializer.data, status.HTTP_200_OK)


class AdvertDeletePhotoView(DestroyAPIView):
    """
    Delete photo from advert
    """

    def get_queryset(self):
        return AdvertisementPhotoModel.objects.filter(advert__user_id=self.request.user.id)

    serializer_class = AdvertisementSerializer

    def perform_destroy(self, instance):
        instance.photo.delete()
        photo = self.get_object()
        photo.delete()


@advert_swagger()
class ActivateAdvertView(GenericAPIView):
    """
    Activate advert
    """

    def get_queryset(self):
        return AdvertisementModel.objects.filter(user_id=self.request.user.id)

    def get_serializer(self, *args, **kwargs):
        pass

    def patch(self, *args, **kwargs):
        advert = self.get_object()
        serializer = AdvertisementSerializer(advert)

        if advert.is_active:
            return Response('Already activated', status.HTTP_400_BAD_REQUEST)

        queryset = AdvertisementModel.objects.filter(user=self.request.user, is_active=True).count()
        if queryset > 0 and not self.request.user.premium:
            return Response("You should have a premium account to post more than 1 ad",
                            status.HTTP_400_BAD_REQUEST)

        if advert.warnings > 0 and advert.warnings % 3 == 0:
            return Response("This ad can no be activated...Wait for the manager verdict!",
                            status.HTTP_400_BAD_REQUEST)

        if check_for_bad_words(advert.description):
            advert.warnings += 1

            if advert.warnings % 3 == 0:
                return Response("This ad can no be activated...Wait for the manager verdict!",
                                status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(f"Description cant contain bad words! To active your ad - edit this in your ads",
                            status.HTTP_400_BAD_REQUEST)

        advert.is_active = True
        advert.save()

        return Response(serializer.data, status.HTTP_200_OK)


@advert_swagger()
class DeactivateAdvertView(GenericAPIView):
    """
    Deactivate advert
    """

    def get_queryset(self):
        return AdvertisementModel.objects.filter(user_id=self.request.user.id)

    def get_serializer(self, *args, **kwargs):
        pass

    def patch(self, *args, **kwargs):
        advert = self.get_object()
        advert.is_active = False
        advert.save()

        serializer = AdvertisementSerializer(advert)
        return Response(serializer.data, status.HTTP_200_OK)


class InformationAboutAdvertView(GenericAPIView):
    """
    Get additional information about advert
    """

    def get_queryset(self):
        return AdvertisementModel.objects.filter(user_id=self.request.user.id, is_active=True)

    def get_serializer(self, *args, **kwargs):
        pass

    @method_decorator(cache_page(60 * 0.3))
    @method_decorator(vary_on_cookie)
    def get(self, *args, **kwargs):
        advert = self.get_object()

        if not self.request.user.premium:
            return Response("You should have a premium account to get additional information",
                            status.HTTP_400_BAD_REQUEST)

        city = advert.city
        car_brand = advert.car_brand
        car_model = advert.car_model
        currency = advert.currency
        price = advert.price

        price_in_usd = price

        if currency == 'EUR':
            price_in_usd = price * 1.074
        if currency == 'UAH':
            price_in_usd = price / 37.453

        # FOR COUNT AVERAGE PRICE IN USD IN CITY
        queryset_sum_city = AdvertisementModel.objects.filter(is_active=True, city=city, car_model=car_model,
                                                              car_brand=car_brand).aggregate(Sum('price'))['price__sum']
        price_sum_in_city = queryset_sum_city - price + price_in_usd

        queryset_count_in_city = AdvertisementModel.objects.filter(is_active=True, city=city, car_model=car_model,
                                                                   car_brand=car_brand).count()
        price_avg_in_city = floor(price_sum_in_city / queryset_count_in_city)

        # FOR COUNT AVERAGE PRICE IN USD IN UKRAINE
        queryset_for_country = AdvertisementModel.objects.filter(is_active=True, car_model=car_model,
                                                                 car_brand=car_brand).aggregate(
            Sum('price'))['price__sum']
        price_sum_in_country = queryset_for_country - price + price_in_usd

        queryset_count_in_country = AdvertisementModel.objects.filter(is_active=True, car_model=car_model,
                                                                      car_brand=car_brand).count()
        price_avg_in_country = floor(price_sum_in_country / queryset_count_in_country)

        # FOR GET VIEWS
        views = advert.views

        return Response({f'Average price(USD) in {city}': price_avg_in_city,
                         f'Average price(USD) in UKRAINE': price_avg_in_country,
                         f'Count of views': views}, status.HTTP_200_OK)


# FOR MANAGER
class ListSuspiciousAdvertsView(ListAPIView):
    """
    Get all suspicious adverts(for manager)
    """
    queryset = AdvertisementModel.objects.filter(warnings__in=[num for num in range(31) if num % 3 == 0 and num > 0],
                                                 is_active=False)
    serializer_class = AdvertisementSerializer
    permission_classes = (IsManager,)


# FOR MANAGER
class ApproveSuspiciousAdvertsView(GenericAPIView):
    """
    Approve suspicious advert(for manager)
    """
    queryset = AdvertisementModel.objects.filter(warnings__in=[num for num in range(31) if num % 3 == 0 and num > 0],
                                                 is_active=False)

    def get_serializer(self, *args, **kwargs):
        pass

    permission_classes = (IsManager,)

    @swagger_auto_schema(responses={status.HTTP_200_OK: SwaggerAdvertSerializer()})
    def patch(self, *args, **kwargs):
        advert = self.get_object()

        if advert.is_active:
            return Response("Already activated", status.HTTP_400_BAD_REQUEST)

        advert.is_active = True
        advert.save()

        serializer = AdvertisementSerializer(advert)
        return Response(serializer.data, status.HTTP_200_OK)


# FOR MANAGER
class DestroyInvalidAdvertView(DestroyAPIView):
    """
    Delete invalid advert(for manager)
    """
    queryset = AdvertisementModel.objects.filter(is_active=False)
    serializer_class = AdvertisementSerializer
    permission_classes = (IsManager,)
