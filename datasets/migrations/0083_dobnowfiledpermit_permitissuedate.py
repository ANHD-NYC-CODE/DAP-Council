# Generated by Django 2.2.4 on 2021-03-21 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0082_dobnowfiledpermit_filingdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='dobnowfiledpermit',
            name='permitissuedate',
            field=models.DateField(blank=True, null=True),
        ),
    ]
