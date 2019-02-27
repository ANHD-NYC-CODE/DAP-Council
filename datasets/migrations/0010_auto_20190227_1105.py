# Generated by Django 2.1.5 on 2019-02-27 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0009_community'),
    ]

    operations = [
        migrations.RenameField(
            model_name='community',
            old_name='borocd',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='council',
            old_name='coundist',
            new_name='id',
        ),
        migrations.AlterField(
            model_name='property',
            name='council',
            field=models.ForeignKey(db_column='council', db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='datasets.Council', to_field='coundist'),
        ),
    ]
