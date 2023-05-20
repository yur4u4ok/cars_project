from rest_framework.serializers import ModelSerializer, RelatedField

from .models import AdvertisementModel, AdvertisementPhotoModel
from core.dataclasses.user_dataclasses import User


class UserAdvertisementSerializer(RelatedField):
    def to_representation(self, value: User):
        return {'id': value.id, 'email': value.email}


class AdvertPhotoSerializer(ModelSerializer):
    class Meta:
        model = AdvertisementPhotoModel
        fields = ('photo',)

    def to_representation(self, instance):
        return instance.photo.url


class AdvertisementSerializer(ModelSerializer):
    user = UserAdvertisementSerializer(read_only=True)
    photos = AdvertPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = AdvertisementModel
        fields = ('id', 'car_brand', 'car_model', 'year', 'price', 'currency', 'description',
                  'city', 'is_active', 'warnings', 'photos', 'views', 'user')
        read_only_fields = ('id', 'is_active', 'warnings', 'views', 'user')
