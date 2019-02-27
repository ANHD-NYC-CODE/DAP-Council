# Generated by Django 2.1.5 on 2019-02-27 16:16

import datasets.utils.BaseDatasetModel
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0008_taxlot'),
    ]

    operations = [
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('shapearea', models.DecimalField(blank=True, decimal_places=10, max_digits=24, null=True)),
                ('shapelength', models.DecimalField(blank=True, decimal_places=10, max_digits=24, null=True)),
                ('geometry', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
            ],
            bases=(datasets.utils.BaseDatasetModel.BaseDatasetModel, models.Model),
        ),
    ]
