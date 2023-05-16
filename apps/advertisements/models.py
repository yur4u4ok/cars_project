from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator

from datetime import datetime

from apps.users.models import UserModel as User

UserModel: User = get_user_model()


class AdvertisementModel(models.Model):
    class Meta:
        db_table = 'advertisements'

    car_brand = models.CharField(max_length=40)
    car_model = models.CharField(max_length=20)
    year = models.IntegerField(validators=[MaxValueValidator(datetime.now().year)])
    price = models.IntegerField()
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    warnings = models.IntegerField(default=0)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='advertisements')
