# Generated by Django 2.2.4 on 2021-04-20 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0083_dobnowfiledpermit_permitissuedate'),
    ]

    operations = [
        migrations.AddField(
            model_name='eviction',
            name='councildistrict',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddConstraint(
            model_name='dobpermitissuedlegacy',
            constraint=models.UniqueConstraint(fields=('bbl', 'bin', 'job', 'permitsino'), name='uuid'),
        ),
    ]
