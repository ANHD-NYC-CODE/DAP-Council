# Generated by Django 2.1.5 on 2019-03-17 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0014_hpdcomplaint_bin'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='doblegacyfiledpermit',
            index=models.Index(fields=['bbl', 'prefilingdate'], name='datasets_do_bbl_b22e01_idx'),
        ),
        migrations.AddIndex(
            model_name='doblegacyfiledpermit',
            index=models.Index(fields=['prefilingdate', 'bbl'], name='datasets_do_prefili_6bc8f9_idx'),
        ),
    ]