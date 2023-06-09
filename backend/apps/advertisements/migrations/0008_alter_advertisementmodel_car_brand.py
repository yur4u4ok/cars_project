# Generated by Django 4.2.1 on 2023-05-17 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0007_advertisementmodel_city_advertisementmodel_currency_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisementmodel',
            name='car_brand',
            field=models.CharField(choices=[('BMW', 'BMW'), ('Volvo', 'Volvo'), ('Mercedes', 'Mercedes'), ('Daewoo', 'Daewoo'), ('Volkswagen', 'Volkswagen'), ('Skoda', 'Skoda'), ('Ford', 'Ford'), ('Nissan', 'Nissan'), ('Renault', 'Renault'), ('Audi', 'Audi'), ('Chevrolet', 'Chevrolet'), ('Peugeot', 'Peugeot'), ('Toyota', 'Toyota'), ('KIA', 'KIA'), ('Hyundai', 'Hyundai'), ('Lexus', 'Lexus'), ('Ferrari', 'Ferrari'), ('Lamborghini', 'Lamborghini'), ('Lada', 'Lada'), ('Dacia', 'Dacia'), ('Opel', 'Opel')], default='BMW', max_length=20),
        ),
    ]
