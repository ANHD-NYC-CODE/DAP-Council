# Generated by Django 2.2.4 on 2021-03-21 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0081_dobnowfiledpermit_currentstatusdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='dobnowfiledpermit',
            name='filingdate',
            field=models.DateField(blank=True, null=True),
        ),
    ]
