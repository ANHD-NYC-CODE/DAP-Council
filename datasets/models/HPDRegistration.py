from django.db import models
from datasets.utils.BaseDatasetModel import BaseDatasetModel
from core.utils.transform import from_csv_file_to_gen, with_bbl, hpd_registrations_address_cleanup
from datasets.utils.validation_filters import is_null, is_older_than
import logging

logger = logging.getLogger('app')


class HPDRegistration(BaseDatasetModel, models.Model):
    download_endpoint = "https://data.cityofnewyork.us/api/views/tesw-yqqr/rows.csv?accessType=DOWNLOAD"

    registrationid = models.IntegerField(primary_key=True, blank=False, null=False)
    bbl = models.ForeignKey('Property', db_column='bbl', db_constraint=False,
                            on_delete=models.SET_NULL, null=True, blank=False)
    bin = models.ForeignKey('Building', db_column='bin', db_constraint=False,
                            on_delete=models.SET_NULL, null=True, blank=True)
    buildingid = models.IntegerField(blank=True, null=True)
    boroid = models.SmallIntegerField(blank=True, null=True)
    boro = models.TextField(blank=True, null=True)
    housenumber = models.TextField(blank=True, null=True)
    lowhousenumber = models.TextField(blank=True, null=True)
    highhousenumber = models.TextField(blank=True, null=True)
    streetname = models.TextField(blank=True, null=True)
    streetcode = models.IntegerField(blank=True, null=True)
    zip = models.TextField(blank=True, null=True)
    block = models.SmallIntegerField(blank=True, null=True)
    lot = models.SmallIntegerField(blank=True, null=True)
    communityboard = models.IntegerField(blank=True, null=True)
    lastregistrationdate = models.DateTimeField(blank=True, null=True)
    registrationenddate = models.DateTimeField(blank=True, null=True)

    @classmethod
    def download(self):
        async_download_file.delay(self.__name__, endpoint)

    @classmethod
    def pre_validation_filters(self, gen_rows):
        for row in gen_rows:
            if is_null(row['registrationid']):
                continue
            yield row

    # trims down new update files to preserve memory
    # uses original header values
    @classmethod
    def update_set_filter(self, csv_reader, headers):
        return csv_reader

    @classmethod
    def transform_self(self, file_path, update=None):
        return self.pre_validation_filters(hpd_registrations_address_cleanup(with_bbl(from_csv_file_to_gen(file_path, update), allow_blank=True)))

    @classmethod
    def seed_or_update_self(self, **kwargs):
        return self.seed_or_update_from_set_diff(**kwargs)

    def __str__(self):
        return str(self.complaintid)