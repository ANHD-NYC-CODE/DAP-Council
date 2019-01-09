from django.db import models
from datasets.utils.BaseDatasetModel import BaseDatasetModel
from core.utils.transform import from_csv_file_to_gen
from datasets.utils.validation_filters import is_null, is_older_than
import logging

logger = logging.getLogger('app')


class HousingLitigation(BaseDatasetModel, models.Model):
    download_endpoint = "https://data.cityofnewyork.us/api/views/59kj-x8nc/rows.csv?accessType=DOWNLOAD"

    litigationid = models.IntegerField(primary_key=True, blank=False, null=False)
    bin = models.ForeignKey('Building', db_column='bin', db_constraint=False,
                            on_delete=models.SET_NULL, null=True, blank=True)
    bbl = models.ForeignKey('Property', db_column='bbl', db_constraint=False,
                            on_delete=models.SET_NULL, null=True, blank=False)
    buildingid = models.IntegerField(blank=True, null=True)
    boro = models.SmallIntegerField(blank=True, null=True)
    housenumber = models.TextField(blank=True, null=True)
    streetname = models.TextField(blank=True, null=True)
    zip = models.TextField(blank=True, null=True)
    block = models.SmallIntegerField(blank=True, null=True)
    lot = models.SmallIntegerField(blank=True, null=True)
    casetype = models.TextField(blank=True, null=True)
    caseopendate = models.DateTimeField(blank=True, null=True)
    casestatus = models.TextField(blank=True, null=True)
    openjudgement = models.TextField(blank=True, null=True)
    findingofharassment = models.TextField(blank=True, null=True)
    findingdate = models.DateTimeField(blank=True, null=True)
    penalty = models.TextField(blank=True, null=True)
    respondent = models.TextField(blank=True, null=True)
    latitude = models.DecimalField(decimal_places=8, max_digits=16, blank=True, null=True)
    longitude = models.DecimalField(decimal_places=8, max_digits=16, blank=True, null=True)
    communitydistrict = models.TextField(blank=True, null=True)
    councildistrict = models.TextField(blank=True, null=True)
    censustract = models.TextField(blank=True, null=True)
    nta = models.TextField(blank=True, null=True)

    @classmethod
    def download(self):
        return self.download_file(self.download_endpoint)

    @classmethod
    def pre_validation_filters(self, gen_rows):
        for row in gen_rows:
            if is_null(row['litigationid']):
                continue
            if 'bbl' in row:
                row['bbl'] = str(row['bbl'])
            yield row

    # trims down new update files to preserve memory
    # uses original header values
    @classmethod
    def update_set_filter(self, csv_reader, headers):
        return csv_reader

    @classmethod
    def transform_self(self, file_path):
        return self.pre_validation_filters(from_csv_file_to_gen(file_path))

    @classmethod
    def seed_or_update_self(self, **kwargs):
        logger.info("Seeding/Updating {}", self.__name__)
        return self.seed_or_update_from_set_diff(**kwargs)

    def __str__(self):
        return str(self.violationid)