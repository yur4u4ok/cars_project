from apps.advertisements.serializers import AdvertisementSerializer


class SwaggerAdvertSerializer(AdvertisementSerializer):
    class Meta(AdvertisementSerializer.Meta):
        fields = ('id', 'car_brand', 'car_model', 'year', 'price', 'currency', 'description',
                  'city', 'is_active', 'warnings', 'photos', 'views', 'user')
