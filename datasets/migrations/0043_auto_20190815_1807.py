# Generated by Django 2.2 on 2019-08-15 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0042_auto_20190810_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foreclosure',
            name='index',
            field=models.TextField(),
        ),
    ]
