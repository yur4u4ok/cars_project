# Generated by Django 4.2.1 on 2023-05-17 15:33

import core.services.upload_car_photo_service
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0005_alter_advertisementphotomodel_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisementphotomodel',
            name='photo',
            field=models.ImageField(blank=True, upload_to=core.services.upload_car_photo_service.upload_to),
        ),
    ]
