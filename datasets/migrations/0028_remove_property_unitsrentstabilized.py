# Generated by Django 2.2 on 2019-04-23 21:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0027_propertyannotation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='unitsrentstabilized',
        ),
    ]
