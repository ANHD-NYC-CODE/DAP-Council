# Generated by Django 2.1.5 on 2019-02-27 16:33

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
                ('model_name', models.CharField(max_length=255, unique=True)),
                ('automated', models.BooleanField(blank=True, null=True)),
                ('update_instructions', models.TextField(blank=True, null=True)),
                ('download_endpoint', models.TextField(blank=True, null=True)),
                ('version', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Update',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rows_updated', models.IntegerField(blank=True, default=0, null=True)),
                ('rows_created', models.IntegerField(blank=True, default=0, null=True)),
                ('total_rows', models.IntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('completed_date', models.DateTimeField(blank=True, null=True)),
                ('task_id', models.CharField(blank=True, max_length=255, null=True)),
                ('dataset', models.ForeignKey(blank=True, help_text='File is required for standard updates, Dataset Name required for join table updates', null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Dataset')),
                ('file', models.ForeignKey(blank=True, help_text='File is required for standard updates, Dataset Name required for join table updates', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='current_file', to='core.DataFile')),
                ('previous_file', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='previous_file', to='core.DataFile')),
                ('task_result', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='django_celery_results.TaskResult')),
            ],
        ),
        migrations.AddField(
            model_name='datafile',
            name='dataset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Dataset'),
        ),
    ]
