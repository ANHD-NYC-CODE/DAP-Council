# Generated by Django 2.2.4 on 2019-09-21 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0054_auto_20190921_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='appdate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='basempdate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='dcasdate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='edesigdate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='landmkdate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='masdate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='polidate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='rpaddate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='zoningdate',
            field=models.DateField(blank=True, null=True),
        ),
    ]