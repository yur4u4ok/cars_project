# Generated by Django 4.2.1 on 2023-05-15 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisementmodel',
            name='warnings',
            field=models.IntegerField(default=0),
        ),
    ]