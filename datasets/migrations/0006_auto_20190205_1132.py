# Generated by Django 2.1 on 2019-02-05 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0005_addressrecord'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='building',
            name='address_search',
        ),
        migrations.RemoveField(
            model_name='building',
            name='high_search',
        ),
        migrations.RemoveField(
            model_name='building',
            name='low_search',
        ),
        migrations.RemoveField(
            model_name='building',
            name='street_search',
        ),
    ]
