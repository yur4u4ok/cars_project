# Generated by Django 4.2.1 on 2023-05-18 22:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0011_advertisementmodel_views'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='advertisementmodel',
            options={'ordering': ('id',)},
        ),
    ]