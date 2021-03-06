# Generated by Django 2.2 on 2019-08-08 14:15

import datasets.utils.BaseDatasetModel
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0040_auto_20190516_2307'),
    ]

    operations = [
        migrations.CreateModel(
            name='PSPreForeclosure',
            fields=[
                ('key', models.TextField(primary_key=True, serialize=False)),
                ('address', models.TextField(blank=True, null=True)),
                ('indexno', models.TextField(blank=True, null=True)),
                ('zipcode', models.TextField(blank=True, null=True)),
                ('creditor', models.TextField(blank=True, null=True)),
                ('neighborhood', models.TextField(blank=True, null=True)),
                ('documenttype', models.TextField(blank=True, null=True)),
                ('schooldistrict', models.TextField(blank=True, null=True)),
                ('lientype', models.TextField(blank=True, null=True)),
                ('buildingclass', models.TextField(blank=True, null=True)),
                ('taxvalue', models.TextField(blank=True, null=True)),
                ('dateadded', models.DateTimeField(blank=True, null=True)),
                ('bldgareasqft', models.IntegerField(blank=True, null=True)),
                ('debtor', models.TextField(blank=True, null=True)),
                ('debtoraddress', models.TextField(blank=True, null=True)),
                ('mortgagedate', models.DateTimeField(blank=True, null=True)),
                ('mortgageamount', models.IntegerField(blank=True, null=True)),
                ('hasphoto', models.TextField(blank=True, null=True)),
                ('bbl', models.ForeignKey(db_column='bbl', db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='datasets.Property')),
            ],
            bases=(datasets.utils.BaseDatasetModel.BaseDatasetModel, models.Model),
        ),
        migrations.CreateModel(
            name='PSForeclosure',
            fields=[
                ('key', models.TextField(primary_key=True, serialize=False)),
                ('indexno', models.TextField(blank=True, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('zipcode', models.TextField(blank=True, null=True)),
                ('neighborhood', models.TextField(blank=True, null=True)),
                ('schooldistrict', models.TextField(blank=True, null=True)),
                ('buildingclass', models.TextField(blank=True, null=True)),
                ('bldgareasqft', models.IntegerField(blank=True, null=True)),
                ('auction', models.DateTimeField(blank=True, null=True)),
                ('auctiontime', models.TextField(blank=True, null=True)),
                ('auctionlocation', models.TextField(blank=True, null=True)),
                ('dateadded', models.DateTimeField(blank=True, null=True)),
                ('plaintiff', models.TextField(blank=True, null=True)),
                ('defendant', models.TextField(blank=True, null=True)),
                ('lien', models.TextField(blank=True, null=True)),
                ('judgment', models.TextField(blank=True, null=True)),
                ('referee', models.TextField(blank=True, null=True)),
                ('plaintiffsattorney', models.TextField(blank=True, null=True)),
                ('foreclosuretype', models.TextField(blank=True, null=True)),
                ('legalprocess', models.TextField(blank=True, null=True)),
                ('hasphoto', models.TextField(blank=True, null=True)),
                ('bbl', models.ForeignKey(db_column='bbl', db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='datasets.Property')),
            ],
            bases=(datasets.utils.BaseDatasetModel.BaseDatasetModel, models.Model),
        ),
        migrations.CreateModel(
            name='Foreclosure',
            fields=[
                ('key', models.TextField(primary_key=True, serialize=False)),
                ('index', models.TextField(unique=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('document_type', models.TextField(blank=True, null=True)),
                ('lien_type', models.TextField(blank=True, null=True)),
                ('date_added', models.DateTimeField(blank=True, null=True)),
                ('creditor', models.TextField(blank=True, null=True)),
                ('debtor', models.TextField(blank=True, null=True)),
                ('mortgage_date', models.TextField(blank=True, null=True)),
                ('mortgage_amount', models.TextField(blank=True, null=True)),
                ('auction', models.DateTimeField(blank=True, null=True)),
                ('foreign_key', models.TextField(blank=True, null=True)),
                ('source', models.TextField(blank=True, null=True)),
                ('bbl', models.ForeignKey(db_column='bbl', db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='datasets.Property')),
            ],
            bases=(datasets.utils.BaseDatasetModel.BaseDatasetModel, models.Model),
        ),
        migrations.AddIndex(
            model_name='pspreforeclosure',
            index=models.Index(fields=['bbl', '-dateadded'], name='datasets_ps_bbl_963b3f_idx'),
        ),
        migrations.AddIndex(
            model_name='pspreforeclosure',
            index=models.Index(fields=['-dateadded'], name='datasets_ps_dateadd_7808b1_idx'),
        ),
        migrations.AddIndex(
            model_name='psforeclosure',
            index=models.Index(fields=['bbl', '-dateadded'], name='datasets_ps_bbl_87c6d7_idx'),
        ),
        migrations.AddIndex(
            model_name='psforeclosure',
            index=models.Index(fields=['-dateadded'], name='datasets_ps_dateadd_aefba5_idx'),
        ),
        migrations.AddIndex(
            model_name='foreclosure',
            index=models.Index(fields=['bbl', '-date_added'], name='datasets_fo_bbl_35ec6c_idx'),
        ),
        migrations.AddIndex(
            model_name='foreclosure',
            index=models.Index(fields=['-date_added'], name='datasets_fo_date_ad_ac0d07_idx'),
        ),
    ]
