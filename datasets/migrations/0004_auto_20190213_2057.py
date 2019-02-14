# Generated by Django 2.1.5 on 2019-02-14 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0003_auto_20190210_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='basempdate',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='dcasdate',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='edesigdate',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='geom',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='landmkdate',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='mapplutof',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='masdate',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='polidate',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='rpaddate',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='zoningdate',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='cd',
            field=models.SmallIntegerField(blank=True, db_index=True, null=True),
        ),
    ]
