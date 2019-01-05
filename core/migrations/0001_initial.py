# Generated by Django 2.1 on 2019-01-05 22:07

import core.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('django_celery_results', '0003_auto_20181106_1101'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=core.models.construct_directory_path)),
                ('uploaded_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('model_name', models.CharField(choices=[('HPDViolation', 'HPDViolation'), ('Building', 'Building'), ('Council', 'Council')], max_length=255, unique=True)),
                ('download_endpoint', models.TextField(blank=True, null=True)),
                ('uploaded_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Update',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(choices=[('HPDViolation', 'HPDViolation'), ('Building', 'Building'), ('Council', 'Council')], max_length=255)),
                ('rows_updated', models.IntegerField(blank=True, default=0, null=True)),
                ('rows_created', models.IntegerField(blank=True, default=0, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('completed_date', models.DateTimeField(blank=True, null=True)),
                ('task_id', models.CharField(blank=True, max_length=255, null=True)),
                ('dataset', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Dataset')),
                ('file', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.DataFile')),
                ('task_result', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='django_celery_results.TaskResult')),
            ],
        ),
        migrations.AddField(
            model_name='datafile',
            name='dataset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Dataset'),
        ),
    ]
