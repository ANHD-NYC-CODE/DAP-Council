from django.db import models
from datasets.models.Base import Base as BaseDataset
from core.utils.transform import to_csv


class HPDViolation(BaseDataset, models.Model):
    unformatted_pk = 'ViolationID'

    violationid = models.IntegerField(primary_key=True, blank=False, null=False)
    bbl = models.ForeignKey('Building', db_column='bbl', db_constraint=False,
                            on_delete=models.SET_NULL, null=True, blank=False)
    buildingid = models.IntegerField(blank=False, null=False)
    registrationid = models.IntegerField(blank=True, null=True)
    boroid = models.CharField(blank=False, null=False, max_length=1)
    borough = models.TextField(db_index=True)
    housenumber = models.TextField()
    lowhousenumber = models.TextField(blank=True, null=True)
    highhousenumber = models.TextField(blank=True, null=True)
    streetname = models.TextField()
    streetcode = models.TextField(blank=True, null=True)
    postcode = models.CharField(max_length=5, blank=True, null=True)
    apartment = models.TextField(blank=True, null=True)
    story = models.TextField(blank=True, null=True)
    block = models.TextField(blank=True, null=True)
    lot = models.TextField(blank=True, null=True)
    class_name = models.CharField(max_length=1)
    inspectiondate = models.DateTimeField(db_index=True, blank=True, null=True)
    approveddate = models.DateTimeField(blank=True, null=True)
    originalcertifybydate = models.DateTimeField(blank=True, null=True)
    originalcorrectbydate = models.DateTimeField(blank=True, null=True)
    newcertifybydate = models.DateTimeField(blank=True, null=True)
    newcorrectbydate = models.DateTimeField(blank=True, null=True)
    certifieddate = models.DateTimeField(blank=True, null=True)
    ordernumber = models.TextField(blank=True, null=True)
    novid = models.IntegerField(blank=True, null=True)
    novdescription = models.TextField(blank=True, null=True)
    novissueddate = models.DateTimeField(blank=True, null=True)
    currentstatusid = models.SmallIntegerField(db_index=True)
    currentstatus = models.TextField(db_index=True)
    currentstatusdate = models.DateTimeField(db_index=True, blank=True, null=True)
    novtype = models.TextField(blank=True, null=True)
    violationstatus = models.TextField(db_index=True)
    latitude = models.DecimalField(decimal_places=8, max_digits=32, blank=True, null=True)
    longitude = models.DecimalField(decimal_places=8, max_digits=32, blank=True, null=True)
    communityboard = models.TextField(blank=True, null=True)
    councildistrict = models.SmallIntegerField(blank=True, null=True)
    censustract = models.TextField(blank=True, null=True)
    bin = models.IntegerField(db_index=True, blank=True, null=True)
    nta = models.TextField(blank=True, null=True)

    @classmethod
    def transform_self(self, file_path):
        return to_csv(file_path)

    @classmethod
    def seed_or_update_self(self, **kwargs):
        return self.seed_from_set_diff(**kwargs)

    def __str__(self):
        return str(self.violationid)
