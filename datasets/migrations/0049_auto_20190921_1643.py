# Generated by Django 2.2.4 on 2019-09-21 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0048_auto_20190921_1603'),
    ]

    operations = [
        migrations.AddField(
            model_name='dobfiledpermit',
            name='permit_subtype',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dobfiledpermit',
            name='permit_type',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dobfiledpermit',
            name='datefiled',
            field=models.DateField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='doblegacyfiledpermit',
            name='dobrundate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='doblegacyfiledpermit',
            name='latestactiondate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='doblegacyfiledpermit',
            name='prefilingdate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='doblegacyfiledpermit',
            name='signoffdate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='doblegacyfiledpermit',
            name='specialactiondate',
            field=models.DateField(blank=True, null=True),
        ),
    ]
