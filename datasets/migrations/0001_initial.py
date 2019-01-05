# Generated by Django 2.1 on 2019-01-05 03:08

import datasets.utils.Base
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('bbl', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('borough', models.TextField(blank=True, null=True)),
                ('block', models.TextField(blank=True, null=True)),
                ('lot', models.TextField(blank=True, null=True)),
                ('cd', models.SmallIntegerField(blank=True, null=True)),
                ('ct2010', models.TextField(blank=True, null=True)),
                ('cb2010', models.TextField(blank=True, null=True)),
                ('schooldist', models.SmallIntegerField(blank=True, null=True)),
                ('zipcode', models.TextField(blank=True, null=True)),
                ('firecomp', models.TextField(blank=True, null=True)),
                ('policeprct', models.TextField(blank=True, null=True)),
                ('healthcenterdistrict', models.SmallIntegerField(blank=True, null=True)),
                ('healtharea', models.TextField(blank=True, null=True)),
                ('sanitboro', models.TextField(blank=True, null=True)),
                ('sanitdistrict', models.SmallIntegerField(blank=True, null=True)),
                ('sanitsub', models.TextField(blank=True, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('original_address', models.TextField(blank=True, null=True)),
                ('zonedist1', models.TextField(blank=True, null=True)),
                ('zonedist2', models.TextField(blank=True, null=True)),
                ('zonedist3', models.TextField(blank=True, null=True)),
                ('zonedist4', models.TextField(blank=True, null=True)),
                ('overlay1', models.TextField(blank=True, null=True)),
                ('overlay2', models.TextField(blank=True, null=True)),
                ('spdist1', models.TextField(blank=True, null=True)),
                ('spdist2', models.TextField(blank=True, null=True)),
                ('spdist3', models.TextField(blank=True, null=True)),
                ('ltdheight', models.TextField(blank=True, null=True)),
                ('splitzone', models.BooleanField(blank=True, null=True)),
                ('bldgclass', models.TextField(blank=True, db_index=True, null=True)),
                ('landuse', models.SmallIntegerField(blank=True, null=True)),
                ('easements', models.TextField(blank=True, null=True)),
                ('ownertype', models.TextField(blank=True, null=True)),
                ('ownername', models.TextField(blank=True, null=True)),
                ('lotarea', models.BigIntegerField(blank=True, null=True)),
                ('bldgarea', models.BigIntegerField(blank=True, null=True)),
                ('comarea', models.BigIntegerField(blank=True, null=True)),
                ('resarea', models.BigIntegerField(blank=True, null=True)),
                ('officearea', models.BigIntegerField(blank=True, null=True)),
                ('retailarea', models.BigIntegerField(blank=True, null=True)),
                ('garagearea', models.BigIntegerField(blank=True, null=True)),
                ('strgearea', models.BigIntegerField(blank=True, null=True)),
                ('factryarea', models.BigIntegerField(blank=True, null=True)),
                ('otherarea', models.BigIntegerField(blank=True, null=True)),
                ('areasource', models.TextField(blank=True, null=True)),
                ('numbldgs', models.IntegerField(blank=True, db_index=True, null=True)),
                ('numfloors', models.DecimalField(blank=True, db_index=True, decimal_places=2, max_digits=8, null=True)),
                ('unitsres', models.IntegerField(db_index=True)),
                ('unitstotal', models.IntegerField(db_index=True)),
                ('lotfront', models.DecimalField(blank=True, decimal_places=3, max_digits=32, null=True)),
                ('lotdepth', models.DecimalField(blank=True, decimal_places=3, max_digits=32, null=True)),
                ('bldgfront', models.DecimalField(blank=True, decimal_places=3, max_digits=32, null=True)),
                ('bldgdepth', models.DecimalField(blank=True, decimal_places=3, max_digits=32, null=True)),
                ('ext', models.TextField(blank=True, null=True)),
                ('proxcode', models.TextField(blank=True, null=True)),
                ('irrlotcode', models.BooleanField(blank=True, null=True)),
                ('lottype', models.TextField(blank=True, null=True)),
                ('bsmtcode', models.TextField(blank=True, null=True)),
                ('assessland', models.BigIntegerField(blank=True, null=True)),
                ('assesstot', models.BigIntegerField(blank=True, null=True)),
                ('exemptland', models.BigIntegerField(blank=True, null=True)),
                ('exempttot', models.BigIntegerField(blank=True, null=True)),
                ('yearbuilt', models.SmallIntegerField(blank=True, db_index=True, null=True)),
                ('yearalter1', models.SmallIntegerField(blank=True, null=True)),
                ('yearalter2', models.SmallIntegerField(blank=True, null=True)),
                ('histdist', models.TextField(blank=True, null=True)),
                ('landmark', models.TextField(blank=True, null=True)),
                ('builtfar', models.DecimalField(blank=True, db_index=True, decimal_places=2, max_digits=8, null=True)),
                ('residfar', models.DecimalField(blank=True, db_index=True, decimal_places=2, max_digits=8, null=True)),
                ('commfar', models.DecimalField(blank=True, db_index=True, decimal_places=2, max_digits=8, null=True)),
                ('facilfar', models.DecimalField(blank=True, db_index=True, decimal_places=2, max_digits=8, null=True)),
                ('borocode', models.TextField(blank=True, db_index=True, null=True)),
                ('condono', models.TextField(blank=True, null=True)),
                ('tract2010', models.TextField(blank=True, null=True)),
                ('xcoord', models.IntegerField(blank=True, null=True)),
                ('ycoord', models.IntegerField(blank=True, null=True)),
                ('zonemap', models.TextField(blank=True, null=True)),
                ('zmcode', models.TextField(blank=True, null=True)),
                ('sanborn', models.TextField(blank=True, null=True)),
                ('taxmap', models.TextField(blank=True, null=True)),
                ('edesignum', models.TextField(blank=True, null=True)),
                ('appbbl', models.TextField(blank=True, db_index=True, null=True)),
                ('appdate', models.DateTimeField(blank=True, null=True)),
                ('plutomapid', models.TextField(blank=True, null=True)),
                ('firm07flag', models.TextField(blank=True, null=True)),
                ('pfirm15flag', models.TextField(blank=True, null=True)),
                ('version', models.TextField(blank=True, db_index=True, null=True)),
                ('lng', models.DecimalField(blank=True, decimal_places=16, max_digits=32, null=True)),
                ('lat', models.DecimalField(blank=True, decimal_places=16, max_digits=32, null=True)),
            ],
            bases=(datasets.utils.Base.Base, models.Model),
        ),
        migrations.CreateModel(
            name='Council',
            fields=[
                ('coundist', models.IntegerField(primary_key=True, serialize=False)),
                ('shapearea', models.DecimalField(blank=True, decimal_places=10, max_digits=24, null=True)),
                ('shapelength', models.DecimalField(blank=True, decimal_places=10, max_digits=24, null=True)),
                ('geometry', django.contrib.postgres.fields.jsonb.JSONField()),
                ('council_member_name', models.TextField(blank=True, null=True)),
            ],
            bases=(datasets.utils.Base.Base, models.Model),
        ),
        migrations.CreateModel(
            name='HPDViolation',
            fields=[
                ('violationid', models.IntegerField(primary_key=True, serialize=False)),
                ('buildingid', models.IntegerField()),
                ('registrationid', models.IntegerField(blank=True, null=True)),
                ('boroid', models.TextField(blank=True, null=True)),
                ('borough', models.TextField(db_index=True)),
                ('housenumber', models.TextField()),
                ('lowhousenumber', models.TextField(blank=True, null=True)),
                ('highhousenumber', models.TextField(blank=True, null=True)),
                ('streetname', models.TextField()),
                ('streetcode', models.TextField(blank=True, null=True)),
                ('postcode', models.TextField(blank=True, null=True)),
                ('apartment', models.TextField(blank=True, null=True)),
                ('story', models.TextField(blank=True, null=True)),
                ('block', models.TextField(blank=True, null=True)),
                ('lot', models.TextField(blank=True, null=True)),
                ('class_name', models.TextField(blank=True, null=True)),
                ('inspectiondate', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('approveddate', models.DateTimeField(blank=True, null=True)),
                ('originalcertifybydate', models.DateTimeField(blank=True, null=True)),
                ('originalcorrectbydate', models.DateTimeField(blank=True, null=True)),
                ('newcertifybydate', models.DateTimeField(blank=True, null=True)),
                ('newcorrectbydate', models.DateTimeField(blank=True, null=True)),
                ('certifieddate', models.DateTimeField(blank=True, null=True)),
                ('ordernumber', models.TextField(blank=True, null=True)),
                ('novid', models.IntegerField(blank=True, null=True)),
                ('novdescription', models.TextField(blank=True, null=True)),
                ('novissueddate', models.DateTimeField(blank=True, null=True)),
                ('currentstatusid', models.SmallIntegerField(db_index=True)),
                ('currentstatus', models.TextField(db_index=True)),
                ('currentstatusdate', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('novtype', models.TextField(blank=True, null=True)),
                ('violationstatus', models.TextField(db_index=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=8, max_digits=32, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=8, max_digits=32, null=True)),
                ('communityboard', models.TextField(blank=True, null=True)),
                ('councildistrict', models.SmallIntegerField(blank=True, null=True)),
                ('censustract', models.TextField(blank=True, null=True)),
                ('bin', models.IntegerField(blank=True, db_index=True, null=True)),
                ('nta', models.TextField(blank=True, null=True)),
                ('bbl', models.ForeignKey(db_column='bbl', db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='datasets.Building')),
            ],
            bases=(datasets.utils.Base.Base, models.Model),
        ),
        migrations.AddField(
            model_name='building',
            name='council',
            field=models.ForeignKey(db_column='council', db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='datasets.Council'),
        ),
    ]
