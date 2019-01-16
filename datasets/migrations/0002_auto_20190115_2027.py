# Generated by Django 2.1 on 2019-01-16 01:27

import datasets.utils.BaseDatasetModel
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HPDProblem',
            fields=[
                ('problemid', models.IntegerField(primary_key=True, serialize=False)),
                ('unittypeid', models.SmallIntegerField(blank=True, null=True)),
                ('unittype', models.TextField(blank=True, null=True)),
                ('spacetypeid', models.SmallIntegerField(blank=True, null=True)),
                ('spacetype', models.TextField(blank=True, null=True)),
                ('typeid', models.SmallIntegerField(blank=True, null=True)),
                ('type', models.TextField(blank=True, null=True)),
                ('majorcategoryid', models.SmallIntegerField(blank=True, null=True)),
                ('majorcategory', models.TextField(blank=True, null=True)),
                ('minorcategoryid', models.SmallIntegerField(blank=True, null=True)),
                ('minorcategory', models.TextField(blank=True, null=True)),
                ('codeid', models.SmallIntegerField(blank=True, null=True)),
                ('code', models.TextField(blank=True, null=True)),
                ('statusid', models.IntegerField(blank=True, db_index=True, null=True)),
                ('status', models.TextField(blank=True, db_index=True, null=True)),
                ('statusdate', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('statusdescription', models.TextField(blank=True, null=True)),
            ],
            bases=(datasets.utils.BaseDatasetModel.BaseDatasetModel, models.Model),
        ),
        migrations.RemoveField(
            model_name='hpdcomplaint',
            name='code',
        ),
        migrations.RemoveField(
            model_name='hpdcomplaint',
            name='codeid',
        ),
        migrations.RemoveField(
            model_name='hpdcomplaint',
            name='majorcategory',
        ),
        migrations.RemoveField(
            model_name='hpdcomplaint',
            name='majorcategoryid',
        ),
        migrations.RemoveField(
            model_name='hpdcomplaint',
            name='minorcategory',
        ),
        migrations.RemoveField(
            model_name='hpdcomplaint',
            name='minorcategoryid',
        ),
        migrations.RemoveField(
            model_name='hpdcomplaint',
            name='problemid',
        ),
        migrations.RemoveField(
            model_name='hpdcomplaint',
            name='spacetype',
        ),
        migrations.RemoveField(
            model_name='hpdcomplaint',
            name='spacetypeid',
        ),
        migrations.RemoveField(
            model_name='hpdcomplaint',
            name='statusdescription',
        ),
        migrations.RemoveField(
            model_name='hpdcomplaint',
            name='type',
        ),
        migrations.RemoveField(
            model_name='hpdcomplaint',
            name='typeid',
        ),
        migrations.RemoveField(
            model_name='hpdcomplaint',
            name='unittype',
        ),
        migrations.RemoveField(
            model_name='hpdcomplaint',
            name='unittypeid',
        ),
        migrations.AddField(
            model_name='hpdproblem',
            name='complaintid',
            field=models.ForeignKey(db_column='complaintid', db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='datasets.HPDComplaint'),
        ),
    ]