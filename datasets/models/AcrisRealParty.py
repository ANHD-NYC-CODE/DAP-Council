from django.db import models
from datasets.utils.BaseDatasetModel import BaseDatasetModel
from core.utils.transform import from_csv_file_to_gen, with_bbl
from datasets.utils.validation_filters import is_null

# ACRIS Real Party
# Links multiple party informations
# To single MasterLegal document by documentid
import logging

logger = logging.getLogger('app')


class AcrisRealParty(BaseDatasetModel, models.Model):
    download_endpoint = 'https://data.cityofnewyork.us/api/views/636b-3b5g/rows.csv?accessType=DOWNLOAD'

    key = models.TextField(primary_key=True, blank=False, null=False)
    documentid = models.ForeignKey('AcrisRealMaster', db_column='documentid', db_constraint=False,
                                   on_delete=models.SET_NULL, null=True, blank=False)
    recordtype = models.TextField(blank=True, null=True)
    partytype = models.SmallIntegerField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    address1 = models.TextField(blank=True, null=True)
    address2 = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    zip = models.TextField(blank=True, null=True)
    goodthroughdate = models.DateTimeField(blank=True, null=True)

    @classmethod
    def download(self):
        return self.download_file(self.download_endpoint)

    @classmethod
    def pre_validation_filters(self, gen_rows):
        for row in gen_rows:
            if is_null(row['documentid']):
                continue
            row['key'] = "{}-{}".format(row['documentid'], ''.join(e for e in row['name'] if e.isalnum()))
            yield row

    # trims down new update files to preserve memory
    # uses original header values
    @classmethod
    def update_set_filter(self, csv_reader, headers):
        return csv_reader

    @classmethod
    def transform_self(self, file_path, update=None):
        return self.pre_validation_filters(with_bbl(from_csv_file_to_gen(file_path, update), allow_blank=True))

    @classmethod
    def seed_or_update_self(self, **kwargs):
        logger.debug("Seeding/Updating {}", self.__name__)
        return self.seed_with_upsert(**kwargs)

    def __str__(self):
        return self.key
