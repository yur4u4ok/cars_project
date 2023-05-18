from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator

from datetime import datetime

from apps.users.models import UserModel as User
from core.services.upload_car_photo_service import upload_to

UserModel: User = get_user_model()


class AdvertisementModel(models.Model):
    class Meta:
        db_table = 'advertisements'

    MODELS_CHOICES = [
        ('BMW', 'BMW'), ('Volvo', 'Volvo'), ('Mercedes', 'Mercedes'), ('Daewoo', 'Daewoo'),
        ('Volkswagen', 'Volkswagen'), ('Skoda', 'Skoda'), ('Ford', 'Ford'), ('Nissan', 'Nissan'),
        ('Renault', 'Renault'), ('Audi', 'Audi'), ('Chevrolet', 'Chevrolet'), ('Peugeot', 'Peugeot'),
        ('Toyota', 'Toyota'), ('KIA', 'KIA'), ('Hyundai', 'Hyundai'), ('Lexus', 'Lexus'), ('Ferrari', 'Ferrari'),
        ('Lamborghini', 'Lamborghini'), ('Lada', 'Lada'), ('Dacia', 'Dacia'), ('Opel', 'Opel')
    ]

    CURRENCY_CHOICES = [
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('UAH', 'UAH'),
    ]

    car_brand = models.CharField(max_length=20, choices=MODELS_CHOICES)
    car_model = models.CharField(max_length=20)
    year = models.IntegerField(validators=[MaxValueValidator(datetime.now().year)])
    price = models.IntegerField()
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    description = models.TextField()
    city = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    warnings = models.IntegerField(default=0)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='advertisements')


class AdvertisementPhotoModel(models.Model):
    class Meta:
        db_table = 'adverts_photo'

    photo = models.ImageField(upload_to=upload_to, blank=True)
    advert = models.ForeignKey(AdvertisementModel, on_delete=models.CASCADE, related_name='photos')
