# Generated by Django 2.1.5 on 2019-02-26 23:04

import datasets.utils.BaseDatasetModel
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0007_fix_eviction_pk'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaxLot',
            fields=[
                ('bbl', models.TextField(primary_key=True, serialize=False)),
                ('condoflag', models.BooleanField(blank=True, db_index=True, null=True)),
                ('condonum', models.CharField(blank=True, max_length=4, null=True)),
                ('coopnum', models.CharField(blank=True, max_length=4, null=True)),
                ('numbf', models.CharField(blank=True, max_length=2, null=True)),
                ('numaddr', models.CharField(blank=True, max_length=4, null=True)),
                ('vacant', models.BooleanField(blank=True, null=True)),
                ('interior', models.BooleanField(blank=True, null=True)),
                ('bbbl', models.ForeignKey(db_column='bbbl', db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='datasets.Property')),
            ],
            bases=(datasets.utils.BaseDatasetModel.BaseDatasetModel, models.Model),
        ),
    ]