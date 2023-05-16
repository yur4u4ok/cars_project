from rest_framework.serializers import ModelSerializer, RelatedField

from .models import AdvertisementModel
from core.dataclasses.user_dataclasses import User


class UserAdvertisementSerializer(RelatedField):
    def to_representation(self, value: User):
        return {'id': value.id, 'email': value.email}


class AdvertisementSerializer(ModelSerializer):
    user = UserAdvertisementSerializer(read_only=True)

    class Meta:
        model = AdvertisementModel
        fields = ('id', 'car_brand', 'car_model', 'year', 'price', 'description',
                  'is_active', 'warnings', 'user')
        read_only_fields = ('id', 'is_active', 'warnings', 'user')
