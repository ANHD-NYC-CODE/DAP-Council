# Generated by Django 2.2.4 on 2021-04-22 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0084_auto_20210420_1957'),
    ]

    operations = [
        migrations.AddField(
            model_name='eviction',
            name='evictionpostcode',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]